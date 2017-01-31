"""This module is responsible for loading question
"""
import os

from document import Document
from question import Question


def string_to_tokens(input_rows):
    """Read our processed file which has list of tab delimited rows
    and convert it to a list of tuples"""
    EXPECTED_COLUMN_LENGTH = 3

    tokens = []
    sentence = []
    for row in input_rows:
        if row == '\n':
            # End of sentence: append to tokens
            if sentence:
                # Only append if sentence is non-empty
                tokens.append(sentence)
                sentence = []
            continue

        row_tokens = row.split()
        assert len(row_tokens) is EXPECTED_COLUMN_LENGTH,\
            'Row {} has {} columns'.format(row, len(row_tokens))

        # Append this token to active sentence
        sentence.append(row_tokens)

    # Append the last sentence
    if sentence:
        tokens.append(sentence)

    return tokens


def get_questions(qn_filepath):
    """Take a question file, and returning
    a list of `Question` objects.
    """
    array = []
    with open(qn_filepath, 'rb') as file:
        for line in file:
            array.append(line)

    delete = ['<top>\r\n', '\r\n', '<desc> Description:\r\n', '</top>\r\n']
    for i in delete:
        array = list(filter((i).__ne__, array))
    final_array = []
    for i in range(len(array)):
        if i % 2 == 0:
            array[i] = array[i].split(' ')[-1].strip()
            array[i+1] = array[i+1].strip().split('?')[0]
            qn = Question(qn_id=int(array[i]), qn_text=array[i+1])
            final_array.append(qn)

    return final_array


def get_documents(path_to_dir, qn_id):
    """Given the question id and path to answers for all questions,
    return the list of documents that contain answers
    """
    files_to_question = []
    directory = os.path.join(path_to_dir, str(qn_id))
    filenames = os.listdir(directory)
    filenames.sort(key=int)

    for filename in filenames:
        doc_name, _ = os.path.splitext(filename)
        document_filepath = os.path.join(directory, filename)
        with open(document_filepath, 'rb') as subfile:
            subfile_data = subfile.readlines()

        # Use tried-and-tested tokenizer code from P1...
        tokenized_sentences = string_to_tokens(subfile_data)
        if not tokenized_sentences:
            continue

        doc = Document(doc_id=int(doc_name), qn_id=qn_id, content=tokenized_sentences)
        files_to_question.append(doc)

    return files_to_question


def test_reader(qn_filepath, answers_dirpath):
    """Convenience method for repeated debugging/testing
    of bugs
    """
    qns = get_questions(qn_filepath)
    for qn in qns:
        if qn.qid == 100:
            q = qn
            break
    assert q
    docs = get_documents(answers_dirpath, q.qid)
    print docs
    print docs[0].content
