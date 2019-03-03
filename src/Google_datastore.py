# Imports the Google Cloud client library
from google.cloud import datastore


class Datastore():

    def __init__(self):
        self.kind = 'question'
        # Instantiates a client
        self.datastore_client = datastore.Client()

    def add_data(self, qn_obj):
        # Saves the entity
        question_key = self.datastore_client.key(self.kind, qn_obj['id'])
        question = datastore.Entity(key=question_key)
        question['image'] = qn_obj['image']
        question['label'] = qn_obj['label']
        question['question'] = qn_obj['question']
        question['audio'] = qn_obj['audio']
        self.datastore_client.put(question)

    def get_data(self):
        client = datastore.Client()
        query = client.query(kind=self.kind)
        return list(query.fetch())

    def delete_data(self, questions):
        keys = [self.datastore_client.key(self.kind, qn['id']) for qn in questions]
        client = datastore.Client()
        client.delete_multi(keys)
