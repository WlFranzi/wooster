"""This module is responsible for taking a `Question`, an answers document
directory, and returning the top-5 `Answer` objects for this `Question`.
These objects contain the required behavior for them to be consumed by the
`output` module
"""
import string

from nltk.corpus import stopwords

from answer import Answer
from preprocess import process_ner_sentence
from question import Question
from reader import get_documents
from utils import log, warn
import re


ENGLISH_STOPWORDS = set(stopwords.words('english'))
PUCTUATIONS = set(string.punctuation)


def strip_function_words(sentence):
    FUNCTION_POS = [
        'IN',  # Preposition or subordinating conjunction
        'PRP', 'PRP$', 'WP', 'WP$',  # Pronoun
        'DT', 'PDT', 'WDT',  # Determiners
        'CC',  # Coordinating conjunction
        'TO',  # To
        'RP',  # Particles
        'MD',  # Modals (Auxillary Verbs)
        'EX',  # Existential "there" clause
        'WRB',  # Where-adverb
    ]
    return [
        (token, pos, ne_label)
        for token, pos, ne_label in sentence
        if pos not in FUNCTION_POS and
        token.lower() not in ENGLISH_STOPWORDS and
        token not in PUCTUATIONS
    ]


def get_time_type_for_words(words):
    months = set([
        'january', 'february', 'march', 'april', 'june',
        'july', 'august', 'september', 'october', 'november',
        'december'
    ])

    timelines = set(['bc', 'ad', 'bce', 'ce'])

    time_labels = [
        token.lower() in months or
        token.lower() in timelines or
        re.compile(r'\d{4}').match(token) is not None or
        re.compile(r'\d+(?:th|rd|st)').match(token) is not None or
        re.compile(r'\'\d{2}').match(token) is not None
        for token in words
    ]

    return time_labels


def strip_function_words_from_question(question):
    tokens = question.text.split()
    sentence = process_ner_sentence(tokens)
    stripped_sentence = strip_function_words(sentence)

    new_tokens, _, _ = zip(*stripped_sentence)
    return new_tokens


def get_ner_classes_for_question(question):
    q_type = question.qtype
    if q_type == Question.TYPE_WHO:
        return set(['PERSON', 'ORGANIZATION'])
    if q_type == Question.TYPE_WHERE:
        return set(['LOCATION', 'GPE', 'FACILITY'])
    if q_type == Question.TYPE_WHEN:
        return set([])


def get_window(tokens, center, half_width):
    start = max(0, center - half_width)
    end = min(len(tokens), center + half_width + 1)
    return tokens[start:end]


def get_answers(question, answers_dirpath):
    log('Answering "{}"'.format(question))

    question.documents = get_documents(answers_dirpath, question.qid)

    question_tokens = strip_function_words_from_question(question)
    q_words = [word.lower() for word in question_tokens]

    all_answers = []
    for doc in question.documents:
        all_answers += get_all_answers_ranked(question, q_words, doc)

    all_answers = list(set(all_answers))
    all_answers.sort(key=lambda x: x.rank, reverse=True)
    size = min(5, len(all_answers))
    if size < 5:
        warn('Found less than 5 answers for "{}". Appending NIL.'.format(question))
        all_answers.append(Answer.Nil(question.qid))
        size += 1

    answers = []
    for answer in all_answers[:size]:
        length = min(10, len(answer.tokens))
        if length < len(answer.tokens):
            warn('Truncating {} word answer to 10 words'.format(len(answer.tokens)))
        answers.append(Answer(answer.qid, answer.doc_id, answer.tokens[:length]))

    return answers


def get_all_answers_ranked(question, question_words, doc):
    """Given a question and a document, get all the answers
    for this question from this document with their respective ranks
    """
    answers = []
    for sentence in doc.content:
        stripped_sentence = strip_function_words(sentence)
        # If there's no useful data, skip this...
        if not stripped_sentence:
            continue

        sentence_words, _, ner_classes = zip(*stripped_sentence)

        if question.qtype == Question.TYPE_WHEN:
            is_timey = get_time_type_for_words(sentence_words)
            ner_matches = [i for i, flag in enumerate(is_timey) if flag]
        else:
            ner_matches = []
            desired_ner_class = get_ner_classes_for_question(question)
            for i, ner_class in enumerate(ner_classes):
                if ner_class in desired_ner_class:
                    ner_matches.append(i)

        # If there is no relevant answer, skip this...
        if not ner_matches:
            continue

        # Extract and rank each relevant window...
        for i in ner_matches:
            candidate = get_window(sentence_words, i, 4)

            score = 0.0
            common = []
            for word in candidate:
                if word.lower() in question_words:
                    common.append(word.lower())
            score = len(common)

            # If there is no relevance, skip this answer...
            if not score:
                continue

            ans = Answer(question.qid, doc.doc_id, candidate)
            ans.rank = score
            answers.append(ans)

    return answers
