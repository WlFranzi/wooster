import os
import re

import click
from nltk import pos_tag, ne_chunk
from nltk.tokenize import (
    sent_tokenize,
    wordpunct_tokenize
)

from utils import log, success, warn


def process_ner_sentence(sent):
    tagged_sent = pos_tag(sent)
    ner_sent = ne_chunk(tagged_sent)
    return [
        (token, pos, ne_label)
        for (token, pos), ne_label in ner_sent.pos()
    ]


def process_ner(input_string):
    result = []
    for sent in input_string:
        processed = process_ner_sentence(sent)
        sentence_rows = ['\t'.join(row) for row in processed]
        result.append('\n'.join(sentence_rows))
        result.append('')
    return result


def string_to_tokens(input_string):
    tokens = []
    input_string = unicode(input_string, errors='ignore')
    sentences = sent_tokenize(input_string)
    for sentence in sentences:
        tokens.append(wordpunct_tokenize(sentence))

    return tokens


def get_content_under_tag(xml_string, tagname):
    start = xml_string.find('<' + tagname.upper() + '>')
    end = xml_string.find('</' + tagname.upper() + '>')

    # Extract xml for this subtree
    xml_subtree_string = xml_string[start:end]

    # Squash the heirarchy and get only text
    content_string = re.sub(r'<\/?[\w =]+>', '', xml_subtree_string)
    return content_string


def get_content(path_to_doc):
    """Given a file on disk, return all the content
    (without metadata) as a raw string without extra annotations
    """
    with open(path_to_doc, 'rb') as subfile:
        # Ignore the initial SMART annotation which is not XML
        subfile_data = subfile.readlines()[1:]

    subfile_xml_str = ''.join(subfile_data)

    content = ''
    for tag in ['TEXT', 'LEADPARA']:
        content += get_content_under_tag(subfile_xml_str, tag)

    return content


@click.command()
@click.argument('input_dir', type=click.Path())
@click.argument('output_dir', type=click.Path())
def cli(input_dir, output_dir):
    success("---NLP Project Three---")
    input_dirpath = os.path.realpath(input_dir)
    output_dirpath = os.path.realpath(output_dir)

    if input_dirpath == output_dirpath:
        raise ValueError('Input and output directories must be different')

    log("{} --> {}".format(input_dirpath, output_dirpath))

    questions = os.listdir(input_dirpath)
    for question_dirname in questions:
        input_question_dirpath = os.path.join(input_dirpath, question_dirname)

        output_question_dirpath = os.path.join(output_dirpath, question_dirname)
        os.makedirs(output_question_dirpath)

        log('Processing question {}...'.format(question_dirname))

        filenames = os.listdir(input_question_dirpath)
        for filename in filenames:
            input_filepath = os.path.join(input_question_dirpath, filename)

            file_content = get_content(input_filepath)

            if not file_content:
                warn('Found no content in document {}:{}'.format(question_dirname, filename))

            tokens = string_to_tokens(file_content)
            ner_chunks = process_ner(tokens)

            output_filepath = os.path.join(output_question_dirpath, filename)
            output_data = '\n'.join(ner_chunks)
            with open(output_filepath, 'w') as output_file:
                output_file.write(output_data)

        log('Wrote to directory {}'.format(output_question_dirpath))

if __name__ == '__main__':
    cli()
