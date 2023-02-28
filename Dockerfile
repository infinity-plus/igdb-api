FROM python:3.10.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY IGDB_API /code/IGDB_API

COPY .env /code/.env

CMD ["python", "-m", "IGDB_API"]