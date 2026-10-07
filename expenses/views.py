import json
import csv
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .forms import UserRegisterForm, ExpenseForm, BudgetForm
from django.contrib.auth import logout
from .models import Expense, Budget

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
    today = timezone.now().date()

    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-created_at')

    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_month_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    budget_obj = Budget.objects.filter(
        user=request.user,
        month__year=today.year,
        month__month=today.month
    ).first()

    budget_amount = budget_obj.amount if budget_obj else 0
    remaining_budget = budget_amount - current_month_expenses

    percentage = 0
    if budget_amount > 0:
        percentage = min(int((current_month_expenses / budget_amount) * 100), 100)

    context = {
        'expenses': expenses,
        'current_month_expenses': current_month_expenses,
        'budget_amount': budget_amount,
        'remaining_budget': remaining_budget, 
        'percentage': percentage,     
        'page_obj': page_obj,         
    }

    return render(request, 'expenses/expense_list.html', context)


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


@login_required
def set_budget_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user

            Budget.objects.update_or_create(
                user=request.user,
                month=budget.month,
                defaults={'amount': budget.amount}
            )
            messages.success(request, 'تم تحديد الميزانية بنجاح!')
            return redirect('expense-list')

    else:
        form = BudgetForm()

    context = {'form': form}
    return render(request, 'expenses/budget_form.html', context)


@login_required
def dashboard_view(request):
    user_expenses = Expense.objects.filter(user=request.user)

    category_data = (
        user_expenses.values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    categories = [item['category__name'] for item in category_data]
    totals = [float(item['total']) for item in category_data]

    categories_json = json.dumps(categories)
    totals_json = json.dumps(totals)

    context = {
        'categories_json': categories_json,
        'totals_json': totals_json,
    }

    return render(request, 'expenses/dashboard.html', context)


@login_required
def export_expenses_csv(request):
    # 1. إنشاء استجابة HTTP وتعيين نوع المحتوى والملف المرفق
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="expenses_report.csv"'

    # 2. إضافة توقيع UTF-8 BOM لضمان قراءة اللغة العربية بوضوح في Excel و WPS
    response.write('\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    
    # 3. كتابة الصف الأول (عناوين الأعمدة)
    writer.writerow(['العنوان', 'المبلغ (ج.م)', 'الفئة', 'التاريخ'])

    # 4. جلب مصاريف المستخدم
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    for expense in expenses:
        category_name = expense.get_category_display() if hasattr(expense, 'get_category_display') else expense.category
        writer.writerow([
            expense.title,
            expense.amount,
            category_name if category_name else 'بدون فئة',
            expense.date.strftime('%Y-%m-%d')
        ])

    return response


@login_required
def export_expenses_pdf_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    context = {'expenses': expenses}
    return render(request, 'expenses/pdf_report.html', context)


def custom_logout_view(request):
    logout(request)
    return redirect('login')