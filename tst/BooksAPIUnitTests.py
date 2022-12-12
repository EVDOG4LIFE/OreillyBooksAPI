import unittest
import requests

class TestBooksAPI(unittest.TestCase):

    # Test the /books/isbn/:isbn endpoint
    def test_get_books_by_isbn(self):
        # Test with an ISBN10
        testISBN = "1593279280"        

        r = requests.get(f"http://localhost:8000/books/isbn/{testISBN}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()["author"], "Eric Matthes")
        self.assertEqual(r.json()["isbn"], "9781593279288")

        # Test with an ISBN13
        testISBN = "9781593279288"
        r = requests.get(f"http://localhost:8000/books/isbn/{testISBN}")
        self.assertEqual(r.json()["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()["author"], "Eric Matthes")
        self.assertEqual(r.json()["isbn"], "9781593279288")

        # Test with an ISBN13 with hyphens
        testISBN = "978-15-9327-9288"
        r = requests.get(f"http://localhost:8000/books/isbn/{testISBN}")
        self.assertEqual(r.json()["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()["author"], "Eric Matthes")
        self.assertEqual(r.json()["isbn"], "9781593279288")

        # Test ISBN10 with hyphens
        isbn = "1-59-3-2-79-280"
        r = requests.get(f"http://localhost:8000/books/isbn/{isbn}")
        self.assertEqual(r.json()["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()["author"], "Eric Matthes")
        self.assertEqual(r.json()["isbn"], "9781593279288")

        # Test with an invalid ISBN
        isbn = "076531178X"
        r = requests.get(f"http://localhost:8000/books/isbn/{isbn}")
        self.assertEqual(r.status_code, 404)

    # Test the /books/title/:title endpoint
    def test_get_books_by_title(self):
        # Test with a valid title
        title = "Python Crash Course, 2nd Edition"
        r = requests.get(f"http://localhost:8000/books/title/{title}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()[0]["author"], "Eric Matthes")
        self.assertEqual(r.json()[0]["isbn"], "9781593279288")

        # Test with an invalid title
        title = "Mistborn: The Final Empire"
        r = requests.get(f"http://localhost:8000/books/title/{title}")
        self.assertEqual(r.status_code, 404)

    # Test the /books/author/:author endpoint
    def test_get_books_by_author(self):
        # Test with a valid author
        testAuthor = "Eric Matthes"
        r = requests.get(f"http://localhost:8000/books/author/{testAuthor}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]["title"], "Python Crash Course, 2nd Edition")
        self.assertEqual(r.json()[0]["author"], "Eric Matthes")
        self.assertEqual(r.json()[0]["isbn"], "9781593279288")

        # Test with multiple authors
        testAuthor = "Phuong Vothihong; Martin Czygan; Ivan Idris; Magnus Vilhelm Persson; Luiz Felipe Martins"
        r = requests.get(f"http://localhost:8000/books/author/{testAuthor}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]["title"], "Python: End-to-end Data Analysis")
    

        # Test with an invalid author
        testAuthor = "Brandon Sanderson"
        r = requests.get(f"http://localhost:8000/books/author/{testAuthor}")
        self.assertEqual(r.status_code, 404)

    # Test the /books/subject/:subject endpoint
    def test_get_books_by_subject(self):
        # Test with a valid subject
        subject = "Python"
        r = requests.get(f"http://localhost:8000/books/subject/{subject}")
        self.assertEqual(r.status_code, 200)

        # Test with an invalid subject
        subject = "Fantasy"
        r = requests.get(f"http://localhost:8000/books/subject/{subject}")
        self.assertEqual(r.status_code, 404)


# Run the tests
if __name__ == "__main__":
    unittest.main()
