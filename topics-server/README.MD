# Topics server

This project is a culmination of different ideas I've had over the years, namely fusing my interest in NLP techniques and libraries and my linguistics background. When MIT's [SciGen](https://pdos.csail.mit.edu/archive/scigen/) project came into being, I became really intrigued by the prospect of generating text from a series of context free grammars (CFGs). Since the NLTK library available in the Python stack is very comprehensive, I chose to use a bulk of it for my purposes.

What intrigued me even more than just the usage of CFGs to generate text, was the prospect of using Hidden Markov models to randomly select text from a training corpus and generating "novel" (read: unique) sentences. Thus, this project came into being.

The intent is to create a corpus of novel text based upon running training samples through the various 'engines' available:

| Engine | Description | Comments |
|--------|-------------|----------|
| `direct`| Directly access text from the file-system | *Not fully tested* |
| `hiddenmarkovmodel` | Uses the NLTK's HiddenMarkovModelTrainer object to sample text | Requires NLTK to be fully installed |
| `simplifiedmarkovchain` | A simplified Markov implementation to randomly select text | *Not fully tested* |
| `cfg`  | Generate novel text from a context free grammar | *Requires NLTK to be installed; this functionality has also not been fully tested*|


I've been heavily involved in a lot of Apache Lucene-based search engine work in the past and thought Elasticsearch would be a great search store to index these novel sentence-based corpora through. I then created a Flask-based
API that would surface 3 gensim-based topic extraction end-points (I plan to call these end-points with an `ng-redux`
Single-Page-Application I am working on).


There are three steps towards getting this server to run:

**Step 1. Invoke elasticsearch instance**

To invoke the elasticsearch instance, run the following command:

```
docker-compose up -d es
```

This will retrieve an image from elasticsearch and run it in the background.

**Step 2: Generate content**

To generate content, first build the `generator` Docker container, via:

```
docker-compose build generator
```

This will take approx. 5-10 minutes to build  on slower machines. Then create a directory called "data" in this
repo's directory.

Lastly, to generate content, run:

```
docker-compose up generator
```

**Step 3: Index Content**

Next, build the indexer. To do so, run the following command:

```
docker-compose build indexer
```

...and run the container:

```
docker-compose up indexer
```

**Step 4. Turn on the API end-point**

Next build the API:

```
docker-compose build api
```

...and turn it on:

```
docker-compose up api
```
