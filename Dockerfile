FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /hometest
COPY requirements.txt /hometest/
RUN pip install -r requirements.txt
COPY . /hometest/