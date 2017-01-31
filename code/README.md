wooster
====
`ask-wooster`. Not as smart as asking Jeeves, but we'll give it an honest go!
## Installation
The project uses the GNU-Make commands for housekeeping. Please have both GNU Make and Python 2.7 installed and available in the system `PATH`. Additionally, please have the `virtualenv` python package installed.

1. Unzip the documents into the `resources/doc_dev` folder
2. `make ask-wooster` and `make check-wooster` for dev-set
3. `make test-wooster` for test-set
4. Note that `make preprocess` and `make preprocess-test` must be done before the corresponding answering steps.

## Workflow

1. Preprocess all answers in corpus to POS tag and NER-class augmented list of sentences
1. Read questions file into memory and parse into tokens
2. For each question, read the entire 100-document folder into memory and parse into a list of paragraphs (which in turn have sentences/tokens) with feature annotations from preprocessing
3. Extract candidate answers from window around tokens with the NER-type we're looking for
4. Compute the ranking-score of the candidate answers
4. For the top 5 answers, create an answer object consisting of the question id, text, and answer-document id
5. Write out the ranked list of answers in the format specified in the instructions, to provided answer file

## Notable Points

* Removes function words from corpus when considering relevance
* Perform Named Entity Recognition (NER) to extract intelligent guesses of answers
* Additional custom NER-like detection of time-types

## References
* Got the list from http://www.myenglishpages.com/site_php_files/vocabulary-lesson-function-words.php
* Meaning of Penn-Treebank POS from https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
