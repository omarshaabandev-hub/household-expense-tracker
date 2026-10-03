from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Expense

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='البريد الالكتروني')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال: شراء مستلزمات بقالة'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
        labels = {
            'title': 'عنوان المصروف',
            'amount': 'المبلغ',
            'category': 'الفئة',
            'date': 'التاريخ',
        }