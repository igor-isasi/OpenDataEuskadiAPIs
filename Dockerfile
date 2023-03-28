FROM python:3

WORKDIR /code

ENV FLASK_APP server.py
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0

RUN pip3 install -r requirements.txt

EXPOSE 5000


CMD ["python3", "server.py"]