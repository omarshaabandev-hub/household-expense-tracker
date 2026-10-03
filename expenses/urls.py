from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # إعادة توجيه المسار الفارغ تلقائياً لصفحة التسجيل أو القائمة
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('expenses/', views.expense_list_view, name='expense-list')
]