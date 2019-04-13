FROM ubuntu:18.04

RUN apt update -y && \
    apt install -y python3-pip python3-dev && \
    pip3 install pipenv

# We copy just the requirements.txt first to leverage Docker cache
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pipenv install

COPY . /app

RUN pipenv run python manage.py db init; \
    pipenv run python manage.py db migrate -m "Initial"; \
    pipenv run python manage.py db upgrade;

EXPOSE 5000

CMD [ "pipenv", "run", "python", "manage.py", "runserver", "--host", "0.0.0.0", "--port", "5000" ]
