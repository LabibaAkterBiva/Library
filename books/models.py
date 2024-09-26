from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', default=False)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    image = models.ImageField(upload_to='books/media/uploads/', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Comment by {self.user.first_name} {self.user.last_name}'
