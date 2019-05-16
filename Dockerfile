FROM python:3.6

RUN pip install flask flask_restplus flask-cors textblob textblob-fr
COPY . /app
WORKDIR /app

RUN  python -m textblob.download_corpora
ENTRYPOINT ["python"]
CMD ["app.py"]
