from __future__ import absolute_import
import logging
from flask_script import Manager
from app import topics_app
from app.corpus.generator import generate
from app.utils.indexer import index

logging.basicConfig(level=logging.INFO)

manager = Manager(topics_app)


@manager.command
def run_indexer():
    index()


@manager.command
def run_generator():
    logging.info("Running generator")
    generate()



if __name__ == "__main__":
    manager.run()
