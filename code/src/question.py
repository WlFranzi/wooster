class Question(object):
    """Represent a question in the system.
    Contain the initialization data, as well as additional runtime
    data to implement required behaviors. Behaviours as required by the `rank` module
    """
    def __init__(self, qn_text, qn_id):
        self.text = qn_text
        self.qid = qn_id
        self.documents = []

    TYPE_WHO = 'Q_WHO'
    TYPE_WHERE = 'Q_WHERE'
    TYPE_WHEN = 'Q_WHEN'

    @property
    def qtype(self):
        if self.text[:3].lower() == 'who':
            return self.TYPE_WHO
        if self.text[:5].lower() == 'where':
            return self.TYPE_WHERE
        if self.text[:4].lower() == 'when':
            return self.TYPE_WHEN

        raise ValueError('Unexpected question type: {}'.format(self.text))

    def __repr__(self):
        return 'Question {}: "{}"'.format(self.qid, self.text)
