#!/usr/bin/env python
from __future__ import absolute_import
import logging
import nltk
import random
import csv
import os
import re
import string
import urllib2
import uuid
from app.config import settings
from nltk.util import ngrams
from nltk import word_tokenize
from nltk.grammar import CFG
from nltk.grammar import PCFG
from nltk.parse.chart import ChartParser
from nltk.grammar import FeatureGrammar
from nltk.parse.featurechart import FeatureChartParser
from nltk.parse.pchart import InsideChartParser
from nltk.parse.generate import generate as generate_text

logging.basicConfig(level=logging.INFO)


class TextGenerator(object):
    '''
    This class is the primary generator of novel text for this application. The
    options available to the project at run-time are governed by the flags
    contained in the 'config/app.fg' file. The methods below aid in the
    generation and construction of novel text by either: 1) a simplified
    Markov Chain generator; 2) an NLTK-based Hidden Markov Model Trainer;
    3) a parsing of Chomsky-normalized CFG-files to generate novel text and,
    lastly;
    4) a simple mechanism that selects words at random from the given corpus of
    text.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def generate_simple_markov_chain_novel_text(self,
                                                corpus,
                                                number_of_words_in_sentence,
                                                number_of_sentences_per_record,
                                                number_of_records):
        '''
        This method generates a simple, randomized extraction of text based
        upon a Markov model.

        Params:
        --------
        - number_of_words_in_sentence (int): An indicator as to the number of
        words to generate in each novel sentence.
        - number_of_sentences_per_record (int): An indicator as to the number
        of sentences per record to generate.
        - number_of_records (int): An indicator as to the total number of
        records to generate.
        Returns: list
        '''
        tokens = word_tokenize(corpus)
        cache = {}
        words = []
        try:
            bigrams = ngrams(tokens, 2)
            for word1, word2 in bigrams:
                key = (word1)
                if key in cache:
                    cache[key].append(word2)
                else:
                    cache[key] = [word2]
            word_size = len(tokens)
            seed = random.randint(0, word_size-2)
            seed_word, next_word = tokens[seed], tokens[seed + 1]
            word1, word2 = seed_word, next_word
            for _ in range(number_of_records):
                for _ in range(number_of_sentences_per_record):
                    for _ in range(number_of_words_in_sentence):
                        words.append(word1)
                        word1, word2 = word2, random.choice(cache[(word1)])
                    words.append(word2)
                [item.replace('. .', '.') for item in words]
        except Exception, error:
            logging.error('TextGenerator: Error occurred - {0}'.format(
                str(error)))
        return words

    def __tag_and_parse_corpus(self, corpus):
        '''
        This is a utility method to aid in the POS tagging a parsing of corpus
        elements

        Params:
        --------
        - corpus (str): The corpus of text that will be tagged and parsed as a
        single string.

        Returns: tuple
        '''
        tag_re = re.compile(r'[*]|--|[^+*-]+')
        tag_set = set()
        symbols = set()
        cleaned_sentences = []
        try:
            sent_tokens = nltk.sent_tokenize(corpus)
            word_tokens = [nltk.word_tokenize(sentence.replace('\'', ''))
                           for sentence in sent_tokens]
            tagged_tokens = [nltk.pos_tag(tokens) for tokens in word_tokens]
            for sequence in tagged_tokens:
                for i in range(len(sequence)):
                    word, tag = sequence[i]
                    symbols.add(word)
                    tag = tag_re.match(tag).group()
                    tag_set.add(tag)
                    sequence[i] = (word, tag)
                cleaned_sentences.append(sequence)
        except Exception, error:
            logging.error('TextGenerator.__tag_and_parse_corpus: Error '
                          'occurred - {0}'.format(str(error)))
        return cleaned_sentences, list(tag_set), list(symbols)

    def generate_hmm_novel_text(self,
                                corpus,
                                number_of_words_in_sentence,
                                number_of_sentences_per_record,
                                number_of_records):
        '''
        This is a method that generates novel text using NLTK's
        HiddenMarkovModelTrainer object

        Params:
        -------
        - number_of_words_in_sentence (int): An indicator as to the number of
        words to generate in each novel sentence.
        - number_of_sentences_per_record (int): An indicator as to the number
        of sentences per record to generate.
        - number_of_records (int): An indicator as to the total number of
        records to generate.

        Returns: list
        '''
        words = []
        punct_selector = ['. ', '! ', '? ']
        punctuation_stop_symbols = dict((ord(char), None) for char in
                                        string.punctuation)
        try:
            labelled_sequence, tag_set, symbols = self.__tag_and_parse_corpus(
                                                                corpus)
            trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)
            hmm = trainer.train_supervised(labelled_sequence,
                                           estimator=lambda fd, bins:
                                           nltk.probability.LidstoneProbDist(
                                            fd, 0.1, bins))
            rng = random.Random(len(corpus))
            for _ in range(number_of_records):
                novel_sentence = []
                for _ in range(number_of_sentences_per_record):
                    sentence = ' '.join(word[0] for word in
                                        hmm.random_sample(rng,
                                        number_of_words_in_sentence))
                    sentence = sentence.translate(punctuation_stop_symbols) + \
                        random.choice(punct_selector)
                    sentence = sentence[0:].capitalize()
                    novel_sentence.append(sentence)
                words.append(''.join(novel_sentence))
        except Exception, error:
            logging.error('TextGenerator.generate_hmm_novel_text: Error '
                          'occurred - {0}'.format(str(error)))
        return words

    def generate_context_free_grammar_novel_text(
                                            self,
                                            corpus,
                                            number_of_words_in_sentence,
                                            number_of_sentences_per_record,
                                            number_of_records):
        '''
        This method utilizes NLTK's Context Free Grammar parser objects to
        parse an available .*cfg file and generate novel text from it.

        Params:
        -------
        - number_of_words_in_sentence (int): An indicator as to the number of
        words to generate in each novel sentence.
        - number_of_sentences_per_record (int): An indicator as to the number
        of sentences per record to generate.
        - number_of_records (int): An indicator as to the total number of
        records to generate.

        Returns: str
        '''
        words = []
        punct_selector = ['. ', '! ', '? ']
        punctuation_stop_symbols = dict((ord(char), None) for char in
                                        string.punctuation)
        parser = None
        grammar = None
        try:
            if isinstance(corpus, CFG):
                _grammar = corpus
                if _grammar is not None:
                    parser = ChartParser(_grammar)
                    grammar = parser.grammar
            elif isinstance(corpus, FeatureGrammar):
                _grammar = corpus
                if _grammar is not None:
                    parser = FeatureChartParser(_grammar)
                    grammar = parser.grammar()
            elif isinstance(corpus, PCFG):
                _grammar = corpus
                if _grammar is not None:
                    parser = InsideChartParser(_grammar)
                    grammar = parser.grammar()
            else:
                grammar = CFG.fromstring(corpus)
            if grammar is not None:
                for _ in range(number_of_records):
                    novel_sentence = []
                    for _ in range(number_of_sentences_per_record):
                        sentence = ' '.join([sent for _, sent in enumerate(
                            generate_text(grammar, depth=2,
                                          n=number_of_words_in_sentence))])
                        sentence = sentence.translate(
                            punctuation_stop_symbols) + random.choice(
                            punct_selector)
                        sentence = sentence[0:].capitalize()
                        novel_sentence.append(sentence)
                    words.append(''.join(novel_sentence))
        except Exception, error:
            logging.error('TextGenerator: Error occurred - {0}'.format(
                          str(error)))
        return '. '.join(words)

    def generate_direct_text(self,
                             corpus,
                             number_of_sentences,
                             number_of_records):
        '''
        This method generates data by randomly selecting words from the corpus
        and assembling them into data records.

        Params:
        -------
        - number_of_sentences (int): An indicator as to the number of sentences
        per record to generate.
        - number_of_records (int): An indicator as to the total number of
        records to generate.

        Returns: list
        '''
        words = []
        sentence_tokens = nltk.sent_tokenize(corpus)
        words = [random.choice(sentence_tokens) for _ in range(
                number_of_sentences) for _ in range(number_of_records)]
        return words

    def generate_csv(self, data, output_file_name, delimiter):
        '''
        This method generates CSV files from the resulting novel text that is
        created by one of the methods above.

        Params:
        -------
        - data (list): The records themselves stored in a list of strings
        - output_file_name (str): The name of the output file
        - delimiter (str): The delimiter used in the csv file
        '''
        try:
            if len(data) > 0:
                abs_path = os.path.abspath(output_file_name)
                with open(abs_path, 'wb') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=delimiter)
                    csv_writer.writerows(data)
            else:
                logging.error('There was an error retrieving the data as an '
                              'array. Its length was zero.')
        except IOError, ioerror:
            logging.error('TextGenerator.generate_csv: IOError occurred - '
                          '{0}'.format(str(ioerror)))
        except Exception, error:
            logging.error('TextGenerator.generate_csv: Error occurred - '
                          '{0}'.format(str(error)))

    def generate_array_of_records(self,
                                  engine_type,
                                  bGenerateUuids,
                                  corpus,
                                  number_of_words_per_sentence,
                                  number_of_sentences_per_record,
                                  number_of_records):
        '''
        This method is a utility method that is charged with invoking the
        different novel text generators above (based upon various 'engines'
        contained in settings).

        Params:
        --------
        - text_generator (obj): The text generator object.
        - engine_type (str): The engine type specified in settings.
        - bGenerateUuids (bool): Parameter that indicates whether GUIDs are to
        be created per record
        - corpus (str): This is the training corpus
        - number_of_words_in_sentence (int): An indicator as to the number of
        words to generate in each novel sentence.
        - number_of_sentences_per_record (int): An indicator as to the number
        of sentences per record to generate.
        - number_of_records (int): An indicator as to the total number of
        records  to generate.

        Returns: list
        '''
        data_obj = []
        if engine_type == 'direct':
            data_obj = self.generate_direct_text(
                            corpus,
                            number_of_sentences_per_record,
                            number_of_records)
        elif engine_type == 'hiddenmarkovmodel':
            data_obj = self.generate_hmm_novel_text(
                                            corpus,
                                            number_of_words_per_sentence,
                                            number_of_sentences_per_record,
                                            number_of_records)
        elif engine_type == 'simplifiedmarkovchain':
            data_obj = self.generate_simple_markov_chain_novel_text(
                            corpus,
                            number_of_words_per_sentence,
                            number_of_sentences_per_record,
                            number_of_records)
        elif engine_type == 'cfg':
            data_obj = self.generate_context_free_grammar_novel_text(
                                            corpus,
                                            number_of_words_per_sentence,
                                            number_of_sentences_per_record,
                                            number_of_records)
        if bGenerateUuids:
            data_obj = [(str(uuid.uuid1()), novel_text) for novel_text in
                        data_obj]
        else:
            data_obj = [(i, novel_text) for i, novel_text in enumerate(
                                                                    data_obj)]
        return data_obj

    def load_nltk_data(self, file_path, prefix):
        '''
        This method loads the NLTK corpus as an object. The path is
        prepended by the prefix 'nltk://' to denote the fact that this corpus
        is from the NLTK's corpora of data.

        Params:
        -------
        - file_path (str): The path to the NTLK file reference
        - prefix (str): The prefix used to denote whether the corpus is part of
                      the NLTK corpora

        Returns: object
        '''
        return nltk.data.load(file_path[len(prefix):])

    def load_nltk_data_as_string(self, file_path, prefix):
        '''
        This method is similar to the one above it except this method returns
        the corpus as a string rather than an object.

        Params:
        -------
        - file_path (str): The path to the NTLK file reference
        - prefix (str): The prefix used to denote whether the corpus is part of
        the NLTK corpora

        Returns: str
        '''
        return nltk.data.load(file_path[len(prefix):], format='text')

    def load_url_data(self, url):
        '''
        This method loads data from a specified URL

        Params:
        -------
        - url (str): URL that contains the data which will be used

        Returns: str
        '''
        response = urllib2.urlopen(url)
        return response.read()

    def load_local_file(self, file_path):
        '''
        This method loads the file specified from the source file system.

        Params:
        ------
        - file_path (str): The relative or absolute path of the data file
        contained on the source file system.

        Returns: str
        '''
        data = ''
        if os.path.isfile(file_path):
            with open(file_path) as local_file:
                data = local_file.read()
        return data


def generate():
    try:
        logging.info('Running generator')
        generator = TextGenerator()
        logging.info('Reference path type = {}'.format(
            settings.CORPORA_REFERENCE_PATH_TYPE))
        if settings.CORPORA_REFERENCE_PATH_TYPE == 'nltk-datafile' and \
           settings.CORPORA_REFERENCE_PATH.startswith('nltk://'):
            if settings.CORPUS_ENGINE_TYPE == 'cfg':
                logging.info('Loading Chomsky-normalized Context Free '
                             'Grammars...')
                raw_data = generator.load_nltk_data_as_string(
                            settings.CORPORA_REFERENCE_PATH, 'nltk://')
            else:
                logging.info('Loading data directly from the NLTK corpora '
                             'stored on the file system...')
                raw_data = generator.load_nltk_data(
                    settings.CORPORA_REFERENCE_PATH, 'nltk://')
        elif settings.CORPORA_REFERENCE_PATH_TYPE == 'local-datafile':
            logging.info('Loading data directly from the file system...')
            raw_data = generator.load_local_file(
                                            settings.CORPORA_REFERENCE_PATH)
        elif settings.CORPORA_REFERENCE_PATH_TYPE == 'url':
            logging.info('Loading data from URLs...')
            raw_data = generator.load_url_data(settings.CORPORA_REFERENCE_PATH)
        if settings.OPERATION_GENERATE_DATA_FILE:
            logging.info('Data-file will be generated utilizing the selected '
                         'engine type: {0}..'.format(
                            settings.CORPUS_ENGINE_TYPE))
            data_obj = generator.generate_array_of_records(
                engine_type=settings.CORPUS_ENGINE_TYPE,
                bGenerateUuids=settings.DATAFILE_GENERATE_UUID,
                corpus=raw_data,
                number_of_words_per_sentence=settings.DATAFILE_WORDS_PER_RECORD,
                number_of_sentences_per_record=settings.DATAFILE_SENTENCES_PER_RECORD,
                number_of_records=settings.DATAFILE_RECORD_NUMBER)
        if data_obj:
            logging.info('Generating CSV files...')
            generator.generate_csv(data_obj,
                                   settings.DATAFILE_OUTPUT_FILE_PATH,
                                   settings.DATAFILE_DELIMITER)
    except Exception, error:
        logging.error(str(error))
