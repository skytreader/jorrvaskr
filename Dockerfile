FROM python:3.7.1-stretch

COPY requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /jorrvaskr/src

ENV FLASK_APP=jorrvaskr.py
CMD ["flask", "run"]
