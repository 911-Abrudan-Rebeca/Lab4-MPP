from django.db import models

# the data you want to present, usually data from a database.
# visible to developer only
# data is created in objects, called Models, and is actually tables in a database.


class Publisher(models.Model):
    publisher = models.CharField(max_length=200, default="0", null=False, unique=True)
    year = models.IntegerField(default="0", null=True)
    owner_name = models.CharField(max_length=200, default="0", null=True)
    format = models.CharField(max_length=200, default="0", null=True)
    country = models.CharField(max_length=200, default="0", null=True)

    def __str__(self):
        return self.publisher


class Books(models.Model):
    name = models.CharField(max_length=200, default='')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    description = models.CharField(max_length=500, default='')
    author = models.CharField(max_length=500, default='')
    review = models.CharField(max_length=500, default='')
    stars = models.IntegerField(default="0")

    def __str__(self):
        return self.name + ' ' + str(self.publisher)


class Customers(models.Model):
    name_of_customer = models.CharField(max_length=200)
    year_of_birth = models.IntegerField(default="0")
    address = models.CharField(max_length=500, default="0")
    gender = models.CharField(max_length=100, default="0")
    phone = models.IntegerField(default="0")

    def __str__(self):
        return str(self.name_of_customer)


class BookSold(models.Model):
    customers_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="customers_id")
    books_id = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="books_id")
    date = models.DateField(default="2000-12-20")
    amount = models.IntegerField(default="0")

    def __str__(self):
        return str(self.customers_id) + " " + str(self.books_id)
