FROM python:3

RUN apt-get update && apt-get -y install sudo

RUN apt install -y firefox-esr

# Establece entorno trabajo
RUN mkdir /crawler
WORKDIR /crawler

# Instala requirements
COPY requirements.txt /crawler
RUN pip3 install -r requirements.txt

COPY . /crawler

# Descarga instalacion web driver
RUN sh gecko_installation.sh

ENTRYPOINT ["python3", "./walla_crawler.py"]