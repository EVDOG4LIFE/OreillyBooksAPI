FROM python:3.7

RUN pip install Flask isbnlib psycopg2

COPY . /app
WORKDIR /app

CMD ["python", "src/app.py"]
