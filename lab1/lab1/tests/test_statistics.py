from rest_framework import status
from rest_framework.reverse import reverse

from lab1.models import Books, Customers
from lab1.models import Publisher, BookSold
from rest_framework.test import APIClient

from lab1.urls import urlpatterns

from django.test import TestCase
from lab1.serializers import serializers, StatisticsSerializerPublisher, StatisticsSerializerCustomer


class statistics_testcase(TestCase):

    def setUp(self):
        publisher1 = Publisher.objects.create(
            publisher='publisher1',
            year=2000,
            owner_name="owner",
            format="format",
            country="testcountry"
        )
        publisher2 = Publisher.objects.create(
            publisher='publisher2',
            year=2000,
            owner_name="owner",
            format="format",
            country="testcountry"
        )
        book1 = Books.objects.create(
            name='book1',
            description='desc',
            author="author",
            review="review",
            stars=5,
            publisher=publisher1
        )
        book2 = Books.objects.create(
            name='book2',
            description='desc',
            author="author",
            review="review",
            stars=5,
            publisher=publisher1
        )
        Books.objects.create(
            name='book3',
            description='desc',
            author="author",
            review="review",
            stars=4,
            publisher=publisher2
        )

        customer1 = Customers.objects.create(
            name_of_customer='customer1',
            year_of_birth=2000,
            address="add",
            gender="f",
            phone=770
        )

        customer2 = Customers.objects.create(
            name_of_customer='customer2',
            year_of_birth=2001,
            address="add",
            gender="f",
            phone=770
        )

        BookSold.objects.create(
            customers_id=customer1,
            books_id=book1,
            date="2000-12-20",
            amount=2
        )

        BookSold.objects.create(
            customers_id=customer2,
            books_id=book2,
            date="2000-12-20",
            amount=1
        )

    # publishers ordered by the average of their books stars
    def test_statistics_publisher(self):
        client = APIClient()
        url = reverse('stat_publisher')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "publisher": "publisher1",
                "avg_stars": 5,
                "book_count": 2
            },
            {
                "id": 2,
                "publisher": "publisher2",
                "avg_stars": 4,
                "book_count": 1
            }

        ]
        serializer = StatisticsSerializerPublisher(expected_data, many=True)
        self.assertEqual(response.data, serializer.data)

    # customers ordered by the average of their books bought amount
    def test_statistics_customers(self):
        client = APIClient()
        url = reverse('stat_customers')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "name_of_customer": "customer1",
                "avg_amount": 2,
                "books_sold_count": 1
            },
            {
                "id": 2,
                "name_of_customer": "customer2",
                "avg_amount": 1,
                "books_sold_count": 1
            }

        ]
        serializer = StatisticsSerializerCustomer(expected_data, many=True)
        self.assertEqual(response.data, serializer.data)
