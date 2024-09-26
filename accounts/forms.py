from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Account

class UserRegisterForm(UserCreationForm):
    birth_day = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    first_name = forms.CharField(widget=forms.TextInput({'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput({'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput({'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'birth_day']

    def save(self, commit=True) :
        our_user = super().save(commit=False)  # Save user first
        if commit == True:
            our_user.save()
            birth_day = self.cleaned_data.get('birth_day')
            Account.objects.create(
                user=self.instance,  # Use the saved user instance
                birth_day=birth_day
            )
            return our_user
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'grow'
                )
            })

class DepositMoneyForm(forms.ModelForm):
    balance = forms.DecimalField()
    class Meta:
        model = Account
        fields = ['balance']

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        MIN_DEPOSIT_AMOUNT = 100
        if balance < MIN_DEPOSIT_AMOUNT:
            raise forms.ValidationError(
                f'You need to deposit at least {MIN_DEPOSIT_AMOUNT}'
            )
        return balance
    
    def __init__(self, *args, **kwargs):
        self.user_account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': ('grow')
            })
    def save(self, commit=True) :
        account = self.user_account
        if commit == True:
            balance = self.cleaned_data.get('balance')
            Account.objects.filter(pk=account.id).update(balance = account.balance + balance)