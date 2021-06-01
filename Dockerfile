FROM python:3.9-buster

RUN mkdir /app
WORKDIR /app

RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install unixodbc-dev -y
RUN apt-get install cloud-init -y

COPY requirements.txt .
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY ./src .

CMD ["python3", "main.py"]
