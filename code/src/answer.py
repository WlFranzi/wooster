class Answer(object):
    """Represent an answer in the system.
    Contain the initialization data, as well as additional runtime
    data to implement required behaviors. Behaviours as required by the
    `rank` and `output` modules
    """
    def __init__(self, qn_id, doc_id, answer_tokens):
        self.qid = qn_id
        self.doc_id = doc_id
        self.tokens = answer_tokens
        self.rank = 0

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text

    @property
    def text(self):
        return ' '.join(self.tokens)

    def __repr__(self):
        return 'Answer {}:{}: {} ({})'.format(self.qid, self.doc_id, self.text, self.rank)

    @staticmethod
    def Nil(qn_id):
        return Answer(qn_id, 0, ['nil'])
