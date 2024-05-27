FROM python:3.10

WORKDIR /usr/src/app

# buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip install --upgrade pip

COPY . /usr/src/app

RUN pip install -r requirements.txt

CMD python3 app.py
