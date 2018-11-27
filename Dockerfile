FROM python:3.7.1-stretch

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV FLASK_APP=/jorrvaskr/app/__init__.py
ENV JORRVASKR_CONFIG=config.Config
ENV JORRVASKR_HOST="0.0.0.0"
CMD ["python", "/jorrvaskr/run.py"]
