FROM python:3.11

ENV PYTHONIOENCODING UTF-8
ENV PYTHONWHITEBYCODE 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /usr/src/app

COPY req.txt ./

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r req.txt

