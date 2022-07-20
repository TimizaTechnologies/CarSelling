"""
Definition of views.
"""

from datetime import datetime
from django.http import HttpRequest
from .models import Car, Contact, Team
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

@login_required
def home(request):
    """Renders the home page."""
    teams = Team.objects.all()
    featured_cars= Car.objects.order_by('-created_date').filter(is_featured=True)
    latest_cars=Car.objects.order_by('-created_date')
    # car_filter_field=Car.objects.values('model', 'city', 'year', 'body_style')
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()

    context = {
        'teams' : teams,
        'home_active': "active",
        'featured_cars': featured_cars,
        'latest_cars':latest_cars,
        # 'car_filter_field':car_filter_field,
        'model_search':model_search,
        'city_search':city_search,
        'year_search':year_search,
        'body_style_search':body_style_search,
        'title':'Home Page',
        'year':datetime.now().year,
    }

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context
    )

def contact(request):
    """Renders the contact page."""
    context={
        'contact_active':"active",
        'title':'Contact',
        'message':'Your contact page.',
        'year':datetime.now().year,
    }

    if request.method=='POST':
        name = request.POST['name']
        email =  request.POST['email']
        subject =  request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        mail_subject = 'You have a message regarding the wheeler website '+ subject
        message_body = 'Name:' + name + ', email:' + email + ', Phone:' +phone

        admin_info = User.objects.get(is_superuser=True)
        admin_email=admin_info.email

        send_mail(
                mail_subject,
                message_body,
                'sample@gmail.com',
                [admin_email],
                fail_silently=False,
                )

        messages.success(request, 'ThankYou for contacting us!')
        return redirect('contact')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context
    )

def about(request):
    """Renders the about page."""
    teams = Team.objects.all()
    context={
        'teams' : teams,
        'about_active':"active",
        'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
    }

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context
    )
    

def services(request):
    context={
        'services_active':"active",
    }
    return render(request, 'app/services.html', context)


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user= auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'app/login.html')

def register(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user=User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password)
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in!')
                    return redirect('dashboard')
                    user.save()
                    messages.success(request, 'You have successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Password didnot Match!')
            return redirect('register')
    else:
        return render(request, 'app/register.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')

@login_required
def cars(request):
    cars_list= Car.objects.order_by('-created_date')
    page = request.GET.get('page')
    paginator=Paginator(cars_list,3)
    paged_cars=paginator.get_page(page)

    #search list naming.
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()


    context={
        'car_active': "active",
        'cars_list':paged_cars,

        'model_search':model_search,
        'city_search':city_search,
        'year_search':year_search,
        'body_style_search':body_style_search,
    }
    return render(request, 'app/cars.html', context)


@login_required
def car_detail(request,id):
    detail= Car.objects.get(id=id)
    context={
        'detail':detail,
    }
    return render(request, 'app/car.html', context)

@login_required
def search(request):
    cars= Car.objects.order_by('-created_date')

    #search list naming
    model_search=Car.objects.values_list('model', flat=True).distinct()
    city_search=Car.objects.values_list('city', flat=True).distinct()
    year_search=Car.objects.values_list('year', flat=True).distinct()
    body_style_search=Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search=Car.objects.values_list('transmission', flat=True).distinct()

    keyword=request.GET.get('keyword')
    if keyword:
        cars=cars.filter(Q(description__icontains=keyword))

    model=request.GET.get('model')
    if model:
        cars=cars.filter(Q(model__icontains=model))

    city=request.GET.get('city')
    if city:
        cars=cars.filter(Q(city__icontains=city))

    year=request.GET.get('year')
    if year:
        cars=cars.filter(Q(year__icontains=year))

    body_style=request.GET.get('body_style')
    if body_style:
        cars=cars.filter(Q(body_style__icontains=body_style))

    transmission=request.GET.get('transmission')
    if transmission:
        cars=cars.filter(Q(transmission__icontains=transmission))


    min_price=request.GET.get('min_price')
    max_price=request.GET.get('max_price')
    if min_price and max_price:
        cars=cars.filter(Q(price__gte=min_price), Q(price__lte=max_price))

    context={
        'cars':cars,

        #search naming list
        'model_search':model_search,
        'city_search':city_search,
        'year_search':year_search,
        'body_style_search':body_style_search,
        'transmission_search':transmission_search,


    }
    return render(request, 'app/search.html', context)


@login_required
def inquiry(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        customer_need=request.POST["customer_need"]
        car_title=request.POST["car_title"]
        city=request.POST["city"]
        state=request.POST["state"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        car_id=request.POST["car_id"]
        user_id=request.POST["user_id"]
        message=request.POST["message"]

        if request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made a request wait until we get back to you!')
                return redirect('/cars/car/'+car_id)

        contact=Contact(first_name=first_name, last_name=last_name, customer_need=customer_need,
        car_title=car_title, city=city, state=state, email=email, phone=phone, car_id=car_id,
        user_id=user_id, message=message)

        admin_info = User.objects.get(is_superuser = True)
        admin_email= admin_info.email
        send_mail(
                'New Car Inquiry',
                'You have a new Inquiry for the car' + car_title + '. Please login to your admin panel for more info.',
                'sahoob193@gmail.com',
                [admin_email],
                fail_silently=False,
                )

        contact.save()
        messages.success(request, 'Your request has been sent!')

        return redirect('/cars/car/'+car_id)