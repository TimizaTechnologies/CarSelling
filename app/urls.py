from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls.static import static
from datetime import datetime

urlpatterns=[
    path('cars/', views.cars, name='cars'),
    path('car/<int:id>', views.car_detail, name='car'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('services/', views.services, name='services'),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]