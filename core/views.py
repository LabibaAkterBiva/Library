
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from categories.models import Category
from books.models import Book

# Create your views here.
def send_email(user, subject, template, data={}):
    html_body = render_to_string(template, {'user':user, 'data':data})
    msg = EmailMultiAlternatives(subject, '', to=[user.email])
    msg.attach_alternative(html_body, 'text/html')
    msg.send()


class Home(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category', None)
        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)
            books = Book.objects.filter(category=category)
        else:
            books = Book.objects.all()
        categories = Category.objects.all()
        context['categories'] = categories
        context['books'] = books
        return context