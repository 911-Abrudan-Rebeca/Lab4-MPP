from django.contrib import admin
from .models import Books, BookSold, Publisher, Customers

admin.site.register(Books)
admin.site.register(Publisher)
admin.site.register(Customers)
admin.site.register(BookSold)
