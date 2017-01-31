class Document(object):
    """Represent a document in the system.
    Contains data about actual file, as well as
    content, and any feature-like data
    """
    def __init__(self, doc_id, qn_id, content):
        # Ensure document has data...
        assert content

        self.doc_id = doc_id
        self.qid = qn_id
        self.content = content
        self.features = {}

    def __repr__(self):
        return 'Document {}:{}'.format(self.qid, self.doc_id)
