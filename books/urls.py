from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:pk>', views.BookDetailsView.as_view(), name='book_details')
]