from rest_framework import serializers
from .models import Books, Publisher, Customers, BookSold

# converting objects into data types understandable by javascript and front-end frameworks (json)
# visible also to clients


class BookSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    review = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(default=0)
    publisher = serializers.SlugRelatedField(queryset=Publisher.objects.all(), slug_field='publisher')

    class Meta:
        model = Books
        fields = ['id', 'name', 'description', 'author', 'review', 'stars', 'publisher']
        # depth = 1

    def validate_stars(self, value):
        if value < 0:
            raise serializers.ValidationError("The number of stars can't be negative")
        if value > 5:
            raise serializers.ValidationError("The number of stars should be maximum 5")
        return value


class BookDetailSerializer(serializers.ModelSerializer):
    customers = serializers.SerializerMethodField(read_only=True)  # for customers buy books

    class Meta:
        model = Books
        fields = ['id', 'name', 'description', 'author', 'review', 'stars', 'publisher', 'customers']
        depth = 1

    # for customers buy books
    def get_customers(self, obj):
        customers = BookSold.objects.filter(books_id=obj)
        return BooksSoldSerializer(customers, many=True).data

    def validate_stars(self, value):
        if value < 0:
            raise serializers.ValidationError("The number of stars can't be negative")
        if value > 5:
            raise serializers.ValidationError("The number of stars should be maximum 5")

        return value


class PublisherSerializer(serializers.ModelSerializer):
    publisher = serializers.CharField(max_length=255)
    owner_name = serializers.CharField(max_length=255)
    format = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    year = serializers.IntegerField(default=0)

    class Meta:
        model = Publisher
        fields = ['id', 'publisher', 'year', 'owner_name', 'format', 'country']

    def validate_year(self, value):
        if value < 1700:
            raise serializers.ValidationError("The year must be >1700.")
        return value


class PublisherDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Publisher
        fields = ['id', 'publisher', 'year', 'owner_name', 'format', 'country', 'books']

    def validate_year(self, value):
        if value < 1700:
            raise serializers.ValidationError("The year must be >1700.")
        return value


class CustomerSerializer(serializers.ModelSerializer):
    name_of_customer = serializers.CharField(max_length=255)
    year_of_birth = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=255)
    phone = serializers.IntegerField(default=0)

    class Meta:
        model = Customers
        fields = ['id', 'name_of_customer', 'year_of_birth', 'address', 'gender', 'phone']

    def validate_phone(self, value):
        if value < 999999999:
            raise serializers.ValidationError("The phone number must be valid (10 digits).")
        return value


class CustomerDetailSerializer(serializers.ModelSerializer):
    books_sold = serializers.SerializerMethodField()  # for customers buy books

    class Meta:
        model = Customers
        fields = ['id', 'name_of_customer', 'year_of_birth', 'address', 'gender', 'phone', 'books_sold']

    def get_books_sold(self, obj):
        books_sold = BookSold.objects.filter(customers_id=obj)
        return BooksSoldSerializer(books_sold, many=True).data

    def validate_phone(self, value):
        if value < 999999999:
            raise serializers.ValidationError("The phone number must be valid (10 digits).")
        return value


class CustomerFilterSerializer(serializers.ModelSerializer):
    year_of_birth = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customers
        fields = ['id', 'year_of_birth']


class BooksSoldSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(default=0)
    date = serializers.DateField(default="2000-12-20")
    customers_id = serializers.SlugRelatedField(queryset=Customers.objects.all(), slug_field='id')
    books_id = serializers.SlugRelatedField(queryset=Books.objects.all(), slug_field='id')

    class Meta:
        model = BookSold
        fields = ['id', 'amount', 'date', 'customers_id', 'books_id']


class BooksSoldDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSold
        fields = ['id', 'amount', 'date', 'customers_id', 'books_id']
        depth = 1


class StatisticsSerializerPublisher(serializers.ModelSerializer):
    avg_stars = serializers.IntegerField(read_only=True)
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Publisher
        fields = ['id', 'publisher', 'avg_stars', 'book_count']


class StatisticsSerializerCustomer(serializers.ModelSerializer):
    avg_amount = serializers.IntegerField(read_only=True)
    books_sold_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customers
        fields = ['id', 'name_of_customer', 'avg_amount', 'books_sold_count']


class BulkAddPublisherWithBooks(serializers.ModelSerializer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.books = serializers.IntegerField(required=False)

    publisher = serializers.CharField(max_length=255)
    owner_name = serializers.CharField(max_length=255)
    format = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    year = serializers.IntegerField(default=0)

    def update_books(self):
        Books.objects.filter(id=int(str(self.publisher))).update(name=self.publisher)

    class Meta:
        model = Publisher
        fields = ['id', 'publisher', 'year', 'owner_name', 'format', 'country']
