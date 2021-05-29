FROM python:3

RUN apt-get update && apt-get -y install sudo

# Establece entorno trabajo
RUN mkdir /crawler
WORKDIR /crawler

# Instala requirements
COPY requirements.txt /crawler
RUN pip3 install -r requirements.txt

COPY . /crawler

# Setup (firefox, gecko, db)
RUN cd setup && sh setup.sh


ENTRYPOINT ["python3", "project/main.py"]