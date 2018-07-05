FROM python:3.5-jessie

WORKDIR /usr/src/app

RUN pip install requests flask pymongo

COPY main.py ./agent.py

CMD ["python", "agent.py"]