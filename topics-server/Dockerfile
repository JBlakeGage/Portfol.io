FROM python:2.7


RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64
RUN chmod +x /usr/local/bin/dumb-init

WORKDIR /code
ADD . /code

VOLUME /data

ADD requirements.txt ./code
RUN pip install --no-cache-dir -r /code/requirements.txt

RUN python -m nltk.downloader maxent_treebank_pos_tagger punkt inaugural

ADD run-as-server /usr/local/bin/run-as-server
RUN chmod +x /usr/local/bin/run-as-server



ENTRYPOINT ["dumb-init"]
CMD ["run-as-server"]
