FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code1
WORKDIR /code1
COPY requirements.txt /code1/
RUN pip install -r requirements.txt
COPY server1/* /code1/
