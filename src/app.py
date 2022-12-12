import flask
import isbnlib
import psycopg2

app = flask.Flask("BooksAPI")

# Import the pool manager from the psycopg2 library
from psycopg2 import pool

# Initiate DB Connection to PostGres DB
DATABASE_URL = "postgres://oreilly:hunter2@localhost:5432/oreilly"

# Create a connection pool
conn_pool = pool.ThreadedConnectionPool(1, 10, DATABASE_URL)


# Define the GET /books/title/:title endpoint
@app.route("/books/title/<title>", methods=["GET"])
def get_books_by_title(title):
    # Query the database for books with the given title
    books = get_books_by_title_query(title)
    # Return 404 error message to user if the book is not found
    if books is None or len(books) == 0:
        return flask.jsonify({
            "error": "Book not found",
            "status": 404
        }), 404 
    # Return the books if they are found
    book_list = []
    for book in books:
        book_list.append({
            "title": book[1],
            "author": book[2],
            "isbn": book[3],
            "description": book[4]
        })
    return flask.jsonify(book_list)

# Define the GET /books/isbn/:isbn endpoint
@app.route("/books/isbn/<isbn>", methods=["GET"])
def get_books_by_isbn(isbn):
    # Remove dashes from the ISBN
    isbn = strip_isbn(isbn)
    # Convert the ISBN10 to ISBN13, if necessary
    isbn = get_isbn13(isbn)
    # Query the database for the book with the given ISBN
    book = get_book_by_isbn_query(isbn)
    # Return 404 error message to user if the book is not found
    if book is None or len(book) == 0:
        return flask.jsonify({
            "error": "Book not found",
            "status": 404
        }), 404 
    # Return the book if it is found
    return flask.jsonify({
        "title": book[1],
        "author": book[2],
        "isbn": book[3],
        "description": book[4]
    })

# Define the GET /books/author/:author endpoint
@app.route("/books/author/<author>", methods=["GET"])
def get_books_by_author(author):
    # Query the database for books with the given author
    books = get_books_by_author_query(author)
    # Return 404 error message to user if the book is not found
    if books is None or len(books) == 0:
        return flask.jsonify({
            "error": "Book not found",
            "status": 404
        }), 404 

    # Return the books if they are found
    book_list = []
    for book in books:
        book_list.append({
            "title": book[1],
            "author": book[2],
            "isbn": book[3],
            "description": book[4]
        })
    return flask.jsonify(book_list)

# Define the GET /books/allISBNs endpoint
@app.route("/books/allISBNs", methods=["GET"])
def get_all_isbns():
    #Query the database for all ISBNs
    isbns = get_all_isbns()

    # Return 404 error message to user if the book is not found
    if isbns is None or len(isbns) == 0:
        return flask.jsonify({
            "error": "Book not found",
            "status": 404
        }), 404

    # Return ISBNs if they are found
    return flask.jsonify({
        "ISBNs": isbns
    })

# Define the get /books/subject/:subject endpoint
@app.route("/books/subject/<subject>", methods=["GET"])
def get_books_by_subject(subject):
    # Query the database for books with the given subject
    books = get_books_by_subject_query(subject)

    # Return 404 error message to user if the book is not found
    if books is None or len(books) == 0:
        return flask.jsonify({
            "error": "Book not found",
            "status": 404
        }), 404

    # Return the books if they are found
    book_list = []
    for book in books:
        book_list.append({
            "title": book[0],
            "author": book[1],
            "isbn": book[2]
        })
    return flask.jsonify(book_list)

# Define variables for endpoints

# DB Query for the GET /books/title/:title endpoint
def get_books_by_title_query(title):
    # Get a connection from the connection pool
    conn = conn_pool.getconn()

    try:
        # Query the database for books with the given title
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.works WHERE title LIKE %s", (f"%{title}%",))
        books = cursor.fetchall()

        # Return the connection to the connection pool
        conn_pool.putconn(conn)
    except Exception as e:
        # Close the connection if an error occurred
        conn_pool.putconn(conn, close=True)
        # Re-raise the error
        raise e

    return books

# DB Query for LIKE books with the given author for the GET /books/author/:author endpoint
def get_books_by_author_query(author):
    # Get a connection from the connection pool
    conn = conn_pool.getconn()

    try:
        # Query the database for books with the given author
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.works WHERE authors LIKE %s", (f"%{author}%",))
        books = cursor.fetchall()

        # Return the connection to the connection pool
        conn_pool.putconn(conn)
    except Exception as e:
        # Close the connection if an error occurred
        conn_pool.putconn(conn, close=True)
        # Re-raise the error
        raise e

    return books

# DB Query for the book with the given ISBN for the GET /books/isbn/:isbn endpoint
def get_book_by_isbn_query(isbn):
    # Get a connection from the connection pool
    conn = conn_pool.getconn()

    try:
        # Query the database for the book with the given ISBN
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM public.works WHERE isbn = %s", (isbn,))
        book = cursor.fetchone()

        # Return the connection to the connection pool
        conn_pool.putconn(conn)
    except Exception as e:
        # Close the connection if an error occurred
        conn_pool.putconn(conn, close=True)
        # Re-raise the error
        raise e

    return book

# DB Query for all ISBNS for the GET /books/allISBNs endpoint
def get_all_isbns():
    # Get a connection from the connection pool
    conn = conn_pool.getconn()

    try:
        # Query the database for all ISBNS
        cursor = conn.cursor()
        cursor.execute("SELECT isbn FROM public.works WHERE isbn != ''")
        isbns = cursor.fetchall()

        # Return the connection to the connection pool
        conn_pool.putconn(conn)
    except Exception as e:
        # Close the connection if an error occurred
        conn_pool.putconn(conn, close=True)
        # Re-raise the error
        raise e

    return isbns

# DB Query for keyword in description with the given subject for the GET /books/subject/:subject endpoint
def get_books_by_subject_query(subject):
#Get a connection from the connection pool
    conn = conn_pool.getconn()

    try:
        # Query the database for books with the given subject
        cursor = conn.cursor()
        cursor.execute("SELECT isbn, title, authors FROM public.works WHERE description LIKE %s", (f"%{subject}%",))
        books = cursor.fetchall()

        # Return the connection to the connection pool
        conn_pool.putconn(conn)
    except Exception as e:
        # Close the connection if an error occurred
        conn_pool.putconn(conn, close=True)
        # Re-raise the error
        raise e

    return books

# Remove hyphens from the ISBN
def strip_isbn(isbn):
    return isbn.replace("-", "")

# Convert the ISBN10 to ISBN13, if necessary
def get_isbn13(isbn):
    if len(isbn) == 10:
        return isbnlib.to_isbn13(isbn)
    return isbn

# Run the app
if __name__ == "__main__":
    app.run(port=8000, debug=True)
