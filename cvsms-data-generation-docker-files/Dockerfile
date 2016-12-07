FROM ubuntu:latest

MAINTAINER PrasannaRishiraj

RUN apt-get update
RUN apt-get install python -y
RUN apt-get install python-pip -y
RUN pip install --upgrade pip

COPY generateData.py generateData.py

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD python generateData.py
