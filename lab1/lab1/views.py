from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from .models import Books, Publisher, Customers, BookSold
from .serializers import BookSerializer, BookDetailSerializer, BooksSoldSerializer, BooksSoldDetailSerializer
from .serializers import StatisticsSerializerPublisher, StatisticsSerializerCustomer
from .serializers import PublisherSerializer, PublisherDetailSerializer
from .serializers import CustomerSerializer, CustomerFilterSerializer, CustomerDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Count
from rest_framework.generics import  GenericAPIView,ListAPIView
from rest_framework.viewsets import ModelViewSet


# A request handler that returns the relevant template and content - based on the request from the user
# takes http requests and returns http response, like HTML documents


class BookAPIView(APIView):
    @api_view(('GET', 'POST'))
    def books_list(request, format=None):

        # get all books
        # serialize them
        # return response (json)

        id = request.query_params.get('id')
        if request.method == 'GET':
            # get id
            if id:
                books = Books.objects.filter(id=id)
            # books = Books.objects.all()
            # serializer = BookSerializer(books, many=True)
            # return JsonResponse({"books": serializer.data})
            # return Response(serializer.data)
            else:
                books = Books.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET', 'PUT', 'DELETE'])
    def books_detail(request, id, format=None):
        try:
            books = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            # get id
            serializer = BookDetailSerializer(books)
            return Response(serializer.data)

        if request.method == 'PUT':
            # update id
            serializer = BookDetailSerializer(books, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            books.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PublisherAPIView(APIView):
    @api_view(['GET', 'POST'])
    def publisher_list(request, format=None):
        if request.method == 'GET':
            publisher = Publisher.objects.all()
            serializer = PublisherSerializer(publisher, many=True)

            return Response(serializer.data)

        if request.method == 'POST':
            serializer = PublisherSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET', 'PUT', 'DELETE'])
    def publisher_detail(request, id, format=None):

        try:
            publisher = Publisher.objects.get(pk=id)
        except Publisher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = PublisherDetailSerializer(publisher)
            return Response(serializer.data)

        elif request.method == 'PUT':
            # update
            serializer = PublisherSerializer(publisher, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            publisher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerAPIView(APIView):
    @api_view(['GET', 'POST'])
    def customer_list(request, format=None):

        if request.method == 'GET':
            customers = Customers.objects.all()
            serializer = CustomerSerializer(customers, many=True)

            return Response(serializer.data)

        if request.method == 'POST':
            serializer = CustomerSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET', 'PUT', 'DELETE'])
    def customer_detail(request, id, format=None):

        try:
            customers = Customers.objects.get(pk=id)
        except Customers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CustomerDetailSerializer(customers)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = CustomerSerializer(customers, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            customers.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @api_view(['GET'])
    def customer_filtered_list(request, year, format=None):

        if request.method == 'GET':

            customers = Customers.objects.filter(year_of_birth__gt=year)

            serializer = CustomerFilterSerializer(customers, many=True)

            return Response(serializer.data)


class BooksSoldAPIView(APIView):
    @api_view(['GET', 'POST'])
    def books_sold_list(request, format=None):

        if request.method == 'GET':
            books_sold = BookSold.objects.all()
            serializer = BooksSoldSerializer(books_sold, many=True)

            return Response(serializer.data)

        if request.method == 'POST':
            serializer = BooksSoldSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @api_view(['GET', 'PUT', 'DELETE'])
    def books_sold_detail(request, id, format=None):

        try:
            books_sold = BookSold.objects.get(pk=id)
        except BookSold.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = BooksSoldDetailSerializer(books_sold)
            # serializer = CustomersBooksSerializer(books_sold)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BooksSoldSerializer(books_sold, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            books_sold.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class Statistics(APIView):
    @api_view(['GET'])
    def statistics_publishers(request):
        # publishers ordered by the average of their books stars
        statistics = Publisher.objects.annotate(
            avg_stars=Avg('books__stars'),
            book_count=Count('books')
        ).order_by('-avg_stars')

        serializer = StatisticsSerializerPublisher(statistics, many=True)
        return Response(serializer.data)

    # done in class
    @api_view(['GET'])
    def statistics_customers(request):
        # customers ordered by the average of their books bought amount
        statistics = Customers.objects.annotate(
            avg_amount=Avg('customers_id__amount'),
            books_sold_count=Count('customers_id')
        ).order_by('-avg_amount')

        serializer = StatisticsSerializerCustomer(statistics, many=True)
        return Response(serializer.data)


class BulkAddView(APIView):
    @csrf_exempt
    @api_view(['POST'])
    def bulkAddPublisherToBook(request):
        book_id_new_publisher_list = request.data.get('book_id_new_publisher_list')

        # Loop through the list of book ids and new publishers to update
        for item in book_id_new_publisher_list:
            books = Books.objects.get(id=item['book_id'])
            books.publisher = Publisher.objects.get(publisher=item['new_publisher'])
            books.save()

        return Response({'message': 'Books updated successfully.'})
