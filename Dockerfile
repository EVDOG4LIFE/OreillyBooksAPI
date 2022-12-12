FROM python:3.7

RUN pip install Flask isbnlib psycopg2

COPY . /app
WORKDIR /app

ENV DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@ormdb:5432/oreilly"

CMD ["python", "app.py"]
