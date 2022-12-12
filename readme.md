O'Reilly Books API
==================

This API provides information on the books available published by O'reilly media. It includes endpoints for retrieving information on all books, a subset of books, and a single book.

Endpoints
---------

### `GET /books`

Returns information on all books in the database.

### `GET /books/title/:title`

Returns information on books matching the specified `title`. 

### `GET /books/isbn/:isbn`

Returns information on a single book with the specified `isbn`. ISBN10 or ISBN13 will be accepted

### `GET /books/author/:author`

Returns information on books with the specified `author` or `authors`.

### `GET /books/subject/:subject`

Returns information on books with the specified `subject` in the description.

Requirements
------------

-   Python 3.7+
-   Flask
-   isbnlib
-   psycopg2

Installation
------------

todo