import os

import click

from rank import get_answers
from reader import get_questions
from utils import (
    error,
    log,
    success,
    warn
    )
from writer import write_answers


@click.command()
@click.argument('question_file', type=click.Path(exists=True))
@click.argument('answers_dir', type=click.Path(exists=True))
@click.argument('answer_file')
@click.option('--test/--no-test', default=False)
def cli(question_file, answers_dir, answer_file, test):
    """Given a set of questions and the answers directory with top 100
    documents for each question, generate the answer file
    """
    success('---NLP Project Three: Question Answer---')

    question_filepath = os.path.realpath(question_file)
    answers_dirpath = os.path.realpath(answers_dir)
    answer_filepath = os.path.realpath(answer_file)

    log('Answering: {}\n Using: {}\n Into: {}'.format(
        question_filepath, answers_dirpath, answer_filepath))

    if test:
        warn('Testing, not normal execution...')
        _test_endpoint(question_filepath, answers_dirpath, answer_filepath)
        return

    try:
        questions = get_questions(question_filepath)
        if len(questions) is not 232:
            warn('devset has 232 questions (Got {})'.format(len(questions)))

        answers = {}
        for question in questions:
            answers[question.qid] = get_answers(question, answers_dirpath)
        if len(answers) is not len(questions):
            warn('Got {} answers for {} questions'.format(len(answers), len(questions)))

        write_answers(answers, answer_filepath)
        success('Wrote answers to {}'.format(answer_filepath))
    except NotImplementedError as e:
        error('TODO: {}'.format(e))


def _test_endpoint(question_filepath, answers_dirpath, answer_filepath):
    """Testing endpoint
    """
    questions = get_questions(question_filepath)
    print questions
    question = [q for q in questions if q.qid == 214]
    print question
    question = question[0]
    answers = get_answers(question, answers_dirpath)
    print answers


if __name__ == '__main__':
    cli()
