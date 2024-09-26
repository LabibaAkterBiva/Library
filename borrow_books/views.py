from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import Borrow
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from accounts.models import Account
from core.views import send_email

# Create your views here.
@login_required
def borrow_book(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=id)
        if book and book.quantity > 0:
           if request.user.account.balance >= book.price:
              book.quantity -= 1
              book.save(update_fields=['quantity'])
              Account.objects.filter(user=request.user).update(balance=request.user.account.balance - book.price)
              Borrow.objects.create(user=request.user, book=book, balance_after_borrow=request.user.account.balance)
              send_email(request.user, 'Borrowed Book', 'borrow_books/borrowMail.html', {'title': book.title})
              messages.success(request, f"You have successfully Borrowed '{book.title}'")
              return redirect('book_details', book.id)
           else:
               messages.warning(request, "You don't have enough balance please deposit some money")
               return redirect('profile')
        else:
            messages.warning(request, 'Sorry this book is not available!!!')
            return redirect('book_details', book.id)
    else:
        messages.warning(request, 'Something is wrong, please try again')
        return redirect('home')

def return_book(request, id):
    if request.method == 'POST':
        borrow  = get_object_or_404(Borrow, pk=id)
        if borrow:
            book = get_object_or_404(Book, pk=borrow.book.id)
            if book:
                book.quantity += 1
                book.save(update_fields=['quantity'])
                Account.objects.filter(user=request.user).update(balance=request.user.account.balance + book.price)
                Borrow.objects.filter(pk=id).update(is_returned=True)
                send_email(request.user, 'Return Book', 'borrow_books/return_mail.html', {'title': book.title})
                messages.success(request, f"You have successfully returned '{book.title}'")
                return redirect('profile')
    else:
        messages.warning(request, 'Something is wrong, please try again')
        return redirect('profile')