from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Book, Review
from .forms import ReviewForm
from django.contrib import messages
from borrow_books.models import Borrow

# Create your views here.
class BookDetailsView(DetailView):
    model = Book
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        context['reviews'] = reviews
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            book = self.get_object()
            borrowed = Borrow.objects.filter(book=book, user=request.user).count()
            if borrowed > 0:
                review_count = Review.objects.filter(book=book, user=request.user).count()
                if review_count < 1:
                    form = ReviewForm(data=self.request.POST)
                    if form.is_valid():
                        review = form.save(commit=False)
                        review.book = book
                        review.user = request.user
                        review.save()
                    return self.get(request, *args, **kwargs)
                else:
                    messages.warning(request, 'It appears you have already submitted a review.')
                    return redirect('book_details', book.id)
            else:
                messages.warning(request, 'Only the user who has borrowed this book can add review')
                return redirect('book_details', book.id)
        else:
            messages.warning(request, 'You are not authenticated. Please login.')
            return redirect('login')


# Create your views here.
