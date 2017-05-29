import os


def is_true(value):
    return value.lower() == 'true'


# Corpus generation engine; options are 'direct' , 'hiddenmarkovmodel',
# 'simplifiedmarkovchain' , 'cfg'
CORPUS_ENGINE_TYPE = os.environ.get("CORPUS_ENGINE_TYPE", "hiddenmarkovmodel")

# Reference path type; options are 'nltk-datafile' , 'local-datafile' , 'url'
CORPORA_REFERENCE_PATH_TYPE = os.environ.get("CORPORA_REFERENCE_PATH_TYPE",
                                             "nltk-datafile")

# Path to the corpus that will be processed.
# Please use the following prefixes: 'nltk://' (for 'nltk-data-file'
# parameter above), 'file://' (for 'local-datafile' parameter above)
# or 'http://' or 'https://' (for 'url' parameter above)
CORPORA_REFERENCE_PATH = os.environ.get("CORPORA_REFERENCE_PATH",
                                        "nltk://corpora/inaugural/"
                                        "1913-Wilson.txt")

# Flag that determines if data-file is to be generated
OPERATION_GENERATE_DATA_FILE = is_true(os.environ.get(
                                "OPERATION_GENERATE_DATA_FILE", "True"))

# Number of records in datafile
DATAFILE_RECORD_NUMBER = int(os.environ.get("DATAFILE_RECORD_NUMBER", 10))

# Number of sentences per record in data file.
DATAFILE_SENTENCES_PER_RECORD = int(os.environ.get(
                                    "DATAFILE_SENTENCES_PER_RECORD", 10))

# Number of words per sentence in data file.
DATAFILE_WORDS_PER_RECORD = int(os.environ.get("DATAFILE_WORDS_PER_RECORD",
                                10))

# Indicates whether uuids should be generated prior to ES indexing
DATAFILE_GENERATE_UUID = is_true(os.environ.get(
                                "DATAFILE_GENERATE_UUID", "True"))

# Path to output datafile
DATAFILE_OUTPUT_FILE_PATH = os.environ.get("DATAFILE_OUTPUT_FILE_PATH",
                                           "output.csv")

# Data-file delimiter
DATAFILE_DELIMITER = os.environ.get("DATAFILE_DELIMITER", "|")

# Flag that determines if data-file is to be indexed into ElasticSearch
OPERATION_INDEX_DATAFILE = is_true(os.environ.get("OPERATION_INDEX_DATAFILE",
                                                  "True"))


# Required to access ElasticSearch instance (e.g. 'http', 'https')
ELASTIC_SEARCH_PROTOCOL = os.environ.get("ELASTIC_SEARCH_PROTOCOL", "http")

# Qualified host-name to ElasticSearch instance
ELASTIC_SEARCH_HOSTNAME = os.environ.get("ELASTIC_SEARCH_HOSTNAME",
                                         "localhost")

# Port number to ElasticSearch instance
ELASTIC_SEARCH_PORT = int(os.environ.get("ELASTIC_SEARCH_PORT", 9200))

# ElasticSearch index name
ELASTIC_SEARCH_INDEX_NAME = os.environ.get("ELASTIC_SEARCH_INDEX_NAME",
                                           "corpus")

# Indicates whether the ElasticSearch should be dropped upon reindexation
DROP_INDEX_FLAG = is_true(os.environ.get("DROP_INDEX_FLAG", "True"))
