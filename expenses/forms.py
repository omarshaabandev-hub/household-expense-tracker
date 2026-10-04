import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Expense, Budget


MONTH_CHOICES = [
    (1, 'يناير (01)'), (2, 'فبراير (02)'), (3, 'مارس (03)'),
    (4, 'أبريل (04)'), (5, 'مايو (05)'), (6, 'يونيو (06)'),
    (7, 'يوليو (07)'), (8, 'أغسطس (08)'), (9, 'سبتمبر (09)'),
    (10, 'أكتوبر (10)'), (11, 'نوفمبر (11)'), (12, 'ديسمبر (12)'),
]

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


class BudgetForm(forms.ModelForm):

    selected_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الشهر'
    )
    selected_year = forms.ChoiceField(
        choices=[(y, str(y)) for y in range(2025, 2031)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='السنة'
    )

    class Meta:
        model = Budget
        fields = ['amount']

        widget = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'أدخل مبلغ الميزانية'}),
        }
        labels = {
            'amount': 'الميزانية الشهرية',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['selected_month'].initial = today.month
        self.fields['selected_year'].initial = today.year

    def save(self, commit=True):
        instance = super().save(commit=False)
        m = int(self.cleaned_data['selected_month'])
        y = int(self.cleaned_data['selected_year'])
        instance.month = datetime.date(y, m, 1)
        if commit:
            instance.save()
        return instance