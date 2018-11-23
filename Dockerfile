FROM python:3.7.1-stretch

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV FLASK_APP=/jorrvaskr/src/jorrvaskr.py
CMD ["flask", "run", "-h", "0.0.0.0"]
