#!/usr/bin/env python
from __future__ import absolute_import
import os
import time
import csv
import logging
from app.config import settings
from datetime import datetime
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO)


class SearchEngineIndexer(object):
    '''
    This is a utility class that handles the indexation of the resulting novel
    text (from the TextGenerator object) into the target
    search engine 'store', which in the case of this project, is Elasticsearch.
    '''

    def __init__(self):
        '''
        Constructor

        Params:
        -------
        searchEngineUrl (str): The indexation url to the search engine; for
        Elasticsearch, this is usually http://localhost:9200
        dropIndex (bool): Flag as to whether the associated index should be
        dropped
        indexName (str): The name of the search index
        '''
        self._searchUrl = settings.ELASTIC_SEARCH_HOSTNAME
        self._dropIndexFlag = settings.DROP_INDEX_FLAG
        self._indexName = settings.ELASTIC_SEARCH_INDEX_NAME

    def __create_base_document(self):
        return {
            'text': '',
            'timestamp': ''
        }

    def __create_indexer_model(self):
        return {
            'index': {
                '_id': '',
                '_type': '',
                '_index': ''
            }
        }

    def __get_search_engine_config(self):
        return {
            'settings': {
                'number_of_shards': 1,
                'number_of_replicas': 0
            }
         }

    def __create_documents(self):
        '''
        This method is charged with creating Elasticsearch documents.

        Params:
        --------
        Returns: list
        '''
        bulk_data = []
        try:
            input_file_path = settings.DATAFILE_OUTPUT_FILE_PATH
            abs_path = os.path.abspath(input_file_path)
            if os.path.isfile(abs_path):
                with open(abs_path, 'r') as csvObj:
                    csv_file = csv.DictReader(
                                        csvObj,
                                        delimiter=settings.DATAFILE_DELIMITER,
                                        fieldnames=['documentId',
                                                    'documentText'])
                    for row in csv_file:
                        _search_index_model = self.__create_indexer_model()
                        _doc_model = self.__create_base_document()
                        _search_index_model['index']['_index'] =  \
                            settings.ELASTIC_SEARCH_INDEX_NAME
                        _search_index_model['index']['_id'] = row['documentId']
                        _search_index_model['index']['_type'] = 'document'
                        _doc_model['text'] = row['documentText']
                        _doc_model['timestamp'] = datetime.now()
                        bulk_data.append(_search_index_model)
                        bulk_data.append(_doc_model)
            else:
                logging.error('There was an error retrieving the CSV file via '
                              'the passed parameters. Please verify accuracy '
                              'of path.')
        except Exception, error:
            logging.error('SearchEngineIndexer.__create_documents: Error '
                          'occured - {}'.format(str(error)))
        return bulk_data

    def ingest_into_es(self, refresh):
        '''
        This method is charged with indexing the documents created above via
        Elasticsearch's Bulk API

        Params:
        --------
        refresh (bool): A flag to determine if the index should be refreshed.
        '''
        es = None
        try:
            es = Elasticsearch(hosts=[{
                'host': settings.ELASTIC_SEARCH_HOSTNAME,
                'port': settings.ELASTIC_SEARCH_PORT
            }])
            bulk_data = self.__create_documents()
            es.bulk(index=settings.ELASTIC_SEARCH_INDEX_NAME,
                    body=bulk_data, refresh=refresh)
        except Exception, error:
            logging.error('SearchEngineIndexer.'
                          'ingest_into_es:'
                          'Error occured - {}'.format(str(error)))


def index():
    indexer = SearchEngineIndexer()
    try:
        if settings.OPERATION_INDEX_DATAFILE:
            logging.info('Datafile with be indexed...')
            indexer = SearchEngineIndexer()
            indexer.ingest_into_es(refresh=True)
    except Exception, error:
        logging.error('Error occurred - {}'.format(error))
