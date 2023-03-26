from unittest import TestCase

from lab1.models import Books


class BookModelTestcase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Books.objects.create(name="Book", publisher="", description="Description", author="Author", review="review", stars=5)

    # def test_string_method(self):
    #     book = Books.objects.get(name="Book")
    #     expected_string = "Book"
    #     self.assertEqual(str(book), expected_string)