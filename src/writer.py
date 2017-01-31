"""This module is responsible for taking a dictionary of answers,
and writing them to file as per the required format
"""


def write_answers(answers, answer_filepath):
    output = open(answer_filepath, 'w')
    for qid in answers:
        ans_set = answers[qid]
        for ans in ans_set:
            line = str(ans.qid) + " " + str(ans.doc_id) + " " + ans.text
            output.write(line + '\n')

    output.close()
