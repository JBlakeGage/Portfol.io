import json
import logging
from app.config import settings
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO)


class Search(object):
    '''
    This class is charged with interfacing with Elasticsearch and parsing the
    resulting response into values that are then passed to the gensim models
    in the 'app.topic' module.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def get(self, search_term=''):
        '''
        This method retrieves the search results returned by Elasticsearch and
        parses them into a list.

        Params:
        -------
        search_term (str): The search term

        Return: list
        '''
        documents = []
        try:
            query = {
              "query": {
                    "bool": {
                        "must": [
                           {
                                "query_string": {
                                    "default_field": "text",
                                    "query": search_term
                                }
                            }
                        ]
                    }
                }
             }
            logging.info('Query = {0}'.format(query))
            es = Elasticsearch(hosts=[{
                'host': settings.ELASTIC_SEARCH_HOSTNAME,
                'port': settings.ELASTIC_SEARCH_PORT
            }])
            data = es.search(index=settings.ELASTIC_SEARCH_INDEX_NAME,
                             body=query)
            for record in data['hits']['hits']:
                result = ''
                result = record.get('_source', {}).get('text', {})
                documents.append(result)
        except Exception, error:
            logging.error('Search.get: Error occurred - {0}'.format(
                          str(error)))
        return documents
