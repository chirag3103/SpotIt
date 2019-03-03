FROM python:3.6.5

ADD . /service
WORKDIR /service

RUN pip install -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=/service/gcp/cc-spotit.json

CMD ["python","App.py"]