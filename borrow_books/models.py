from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.
class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    created_on = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False)
    balance_after_borrow = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return self.book.title