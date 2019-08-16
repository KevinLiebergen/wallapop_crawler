FROM python:3

RUN apt-get update && apt-get -y install sudo

RUN mkdir /crawler

WORKDIR /crawler

COPY requirements.txt /crawler

RUN pip3 install -r requirements.txt

COPY . /crawler

RUN sh gecko_installation.sh

CMD ["python3", "./crawler_walla.py"]