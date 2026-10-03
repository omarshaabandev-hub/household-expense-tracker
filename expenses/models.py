from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=25)
    icon = models.CharField(max_length=10, default='📂', help_text='رمز إيموجي تعبيري للفئة')

    def __str__(self):
        return f"{self.icon} {self.name}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M')

    def __str__(self):
        return f'{self.title} - {self.amount}'


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text='تاريخ يمثل الشهر والسنة للميزانية')

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
