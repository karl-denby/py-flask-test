FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN python manage.py db init; \
    python manage.py db migrate -m "Initial"; \
    python manage.py db upgrade;

ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD [ "manage.py", "runserver", "--host", "0.0.0.0", "--port", "5000" ]
