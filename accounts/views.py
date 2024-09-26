from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .forms import UserRegisterForm, DepositMoneyForm
from django.views.generic import FormView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import Account
from borrow_books.models import Borrow
from core.views import send_email
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email(self.request.user, 'Account created', 'accounts/register_mail.html')
        messages.success(self.request, 'User successfully register and login')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrow_list = Borrow.objects.filter(user=self.request.user)
        context["borrow_list"] = borrow_list
        return context
    

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self) -> str:
        messages.success(self.request, f'Welcome Back {self.request.user.first_name} {self.request.user.last_name}')
        return reverse_lazy('profile')
@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
@method_decorator(login_required, name='dispatch')
class DepositMoneyView(CreateView):
    form_class = DepositMoneyForm
    model = Account
    template_name = 'accounts/deposit.html'
    def get_success_url(self) -> str:
        return reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def form_valid(self, form):
        balance  = form.cleaned_data.get('balance')
        form.save()
        send_email(self.request.user, 'Deposit Money', 'accounts/deposit_mail.html', {'amount': balance})
        messages.success(self.request, f'{balance} has been deposited to your account')
        return super().form_valid(form)