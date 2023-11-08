from django.urls import path
from .views import bookstore

urlpatterns = [
    path('book', bookstore,  name='book'),
]