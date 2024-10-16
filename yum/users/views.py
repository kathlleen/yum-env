from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import UserLoginForm, CustomerRegistrationForm, RestaurantAdminRegistrationForm,CourierRegistrationForm

from users.models import CustomUser


# Create your views here.
def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

                if user.is_restaurant_admin():
                    restaurant = user.restaurant  # Получаем ресторан, которым управляет админ
                    return render(request, 'restaurans/restaurant_dashboard.html', {'restaurant': restaurant})


                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserLoginForm()

    context = {
        'title' : "Authorization",
        'form': form,
    }
    return render(request, 'users/login.html',context)



def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            user = form.instance
            auth.login(request, user)

            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CustomerRegistrationForm()


    context = {
        'title' : "Registration",
        'form' : form,
        'url': 'users:register_customer'
    }
    return render(request, 'users/registration.html',context)


@user_passes_test(lambda u: u.is_superuser)
def register_restaurant_admin(request):
    if request.method == 'POST':
        form = RestaurantAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Устанавливаем тип пользователя как администратор ресторана
            user.user_type = 'restaurant_admin'
            user.save()
        return HttpResponseRedirect(reverse('main:index'))
    else:
        form = RestaurantAdminRegistrationForm()

    context = {
        'title': "Registration restaurant admin",
        'form': form,
        'url' : 'users:register_restaurant_admin'
    }
    return render(request, 'users/registration.html', context)




@user_passes_test(lambda u: u.is_superuser)
def register_courier(request):
    if request.method == 'POST':
        form = CourierRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CourierRegistrationForm()

    context = {
        'title': "Registration courier",
        'form': form,
        'url': 'users:register_courier'
    }
    return render(request, 'users/registration.html', context)