from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
    return render(request, 'expenses/expense_list.html')


def custom_logout_view(request):
    logout(request)
    return redirect('login')