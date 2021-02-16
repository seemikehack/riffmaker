FROM python:3.8
RUN pip install pipenv
COPY Pipfile* /tmp
RUN cd /tmp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app

CMD [ "python", "/app/riffmaker.py" ]
