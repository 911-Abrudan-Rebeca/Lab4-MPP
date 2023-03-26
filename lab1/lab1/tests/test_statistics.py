from rest_framework import status
from rest_framework.reverse import reverse

from lab1.models import Books
from lab1.models import Publisher
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
        Books.objects.create(
            name='book1',
            publisher=publisher1,
            description='desc',
            author="author",
            review="review",
            stars=5
        )
        Books.objects.create(
            name='book2',
            publisher=publisher1,
            description='desc',
            author="author",
            review="review",
            stars=5
        )
        Books.objects.create(
            name='book1',
            publisher=publisher2,
            description='desc',
            author="author",
            review="review",
            stars=5
        )

    def test_statistic(self):
        client = APIClient()
        url = reverse('stat')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 1,
                "name": "publisher1",
                "avg_production_year": 2005,
                "car_count": 2
            },
            {
                "id": 2,
                "name": "brand2",
                "avg_production_year": 2000,
                "car_count": 1
            }
        ]
        serializer = StatisticSerializer(expected_data, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_statistic2(self):
        client = APIClient()
        url = reverse('stat2')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {
                "id": 2,
                "name": "brand2",
                "avg_hp": 200,
                "car_count": 1
            },
            {
                "id": 1,
                "name": "brand1",
                "avg_hp": 125,
                "car_count": 2
            }

        ]
        serializer = StatisticFoundingSerializer(expected_data, many=True)
        self.assertEqual(response.data, serializer.data)