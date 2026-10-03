from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Expense

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('expense-list')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'تم إنشاء الحساب بنجاح لـ {username}! يمكنك تسجيل الدخول الآن.')
            return redirect('login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'expenses/register.html', {'form': form})


@login_required
def expense_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-created_at')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_create_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'تمت اضافة المصروف بنجاح!')
            return redirect('expense-list')
    else:
        form = ExpenseForm()

    context = {
        'form': form,
        'title': 'اضافة مصروف جديد',
    }
    return render(request, 'expenses/expense_form.html', context)


@login_required
def expense_update_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث المصروف بنجاح!')
            return redirect('expense-list')
    else:
        form = ExpenseForm(instance=expense)

    context = {
        'form': form,
        'title': 'تعديل المصروف'
    }
    return render(request, 'expenses/expense_form.html', context)


@login_required
def expense_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'تم حذف المصروف بنجاح!')
        return redirect('expense-list')

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


def custom_logout_view(request):
    logout(request)
    return redirect('login')