FROM python:3-slim-stretch

RUN pip install pipenv
COPY . /src

WORKDIR /src
RUN pipenv install

CMD ["pipenv", "run", "/src/register_servers.py"]
