FROM python:3.9

ADD . /

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD python src/assistant/main.py