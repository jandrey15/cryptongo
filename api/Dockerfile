FROM python:3.5-jessie

ENV FLASK_APP api.py

WORKDIR /usr/src/app

RUN pip install requests flask pymongo

COPY main.py ./api.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]