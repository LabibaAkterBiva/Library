from django.urls import path
from . import views

urlpatterns = [
    path('borrow-book/<int:id>', views.borrow_book, name='borrow_book'),
    path('return-book/<int:id>', views.return_book, name='return_book')
]