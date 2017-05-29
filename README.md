# Portfol.io

***Preamble***

This GitHub repo consists of a series of code-bases which I have created to demonstrate the types of projects that I enjoy coding and developing. My current interests pertain to building advanced analytics utilizing unstructured text processing methodologies (e.g NLP, NER, amongst others).

While much of my professional expertise surrounds traditional web-application creation/building/maintenance/etc., there are many powerful tools in the Python and Java "universes" which align with my stated interests above.

The code in this repo is free to use, however I make no claims as its efficacy or whether it can be used within Production environments; it is merely for illustrative purposes and to provide context for how I would solve specific analysis problems. In other words, please feel free to use this code - but, do so at your own risk...

***Files in this Repository***


The initial project listed is an RESTful topic extraction tool called ["topics-server"](https://github.com/JBlakeGage/Portfol.io/topics-server). It is oriented around REST-like endpoints facilitated by a small Python 2.7 and Docker-based Flask app. It uses the gensim stack to perform 'JSON-ified' TF-IDF, LDA and LSI operations against a corpus of text and is currently designed to search Elasticsearch indexes. It is functional, provided Elasticsearch is online and an index has been created.

The second ["project"](https://github.com/JBlakeGage/Portfol.io/jupyter-notebooks) is a series of IPython notebooks (hosted in Jupyter) that utilize Data-science-relevant techniques that interest me.

The third project is a Python 2.7 and Flask-based clustering tool called ["FlaskLingo"](https://github.com/JBlakeGage/Portfol.io/FlaskLingo). It is based on the ["Lingo" clustering algorithm](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.9.5370&rep=rep1&type=pdf). It uses NLTK, Numpy and scikit-learn and *is currently a work in progress*. The known gaps are: it does not yet calculate cosine similarities between candidate labels, identify label groups that exceed the label similarity threshold or create cluster label candidates. My tentative plan is to incorporate hypernym and meronym detection once the base functionality is completed. *I have provided this for illustration purposes only*.







```  
