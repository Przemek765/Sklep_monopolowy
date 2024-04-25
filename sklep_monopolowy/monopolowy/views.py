from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
import django.contrib.auth


# Create your views here.
def index(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    else:
        context['not_authenticated'] = True

    return render(request, 'monopolowy/home.html', context)


def profile(request):
    return render(request, 'monopolowy/profile.html')


def logout(request):
    django.contrib.auth.logout(request)
    return redirect('monopolowy/index')


def zamowienia(request):
    return render(request, 'monopolowy/zamowienia.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('monopolowy/profile')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    django.contrib.auth.login(request, user)
                    return redirect('monopolowy/index')
        else:
            form = AuthenticationForm()
        return render(request, 'monopolowy/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            django.contrib.auth.login(request, user)
            return redirect('monopolowy/index')
    else:
        form = UserCreationForm()
    return render(request, 'monopolowy/register.html', {'form': form})
