from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import django.contrib.auth
from django.views.generic import UpdateView

from .models import Zamowienie, Asortyment


# Create your views here.
def index(request):
    context = {
        'logged_as_admin': request.user.is_superuser,
        'username': request.user.username,
    }

    return render(request, 'monopolowy/home.html', context)


def profile(request):
    context = {
        'logged_as_admin': request.user.is_superuser,
    }
    return render(request, 'monopolowy/profile.html', context)


def logout(request):
    django.contrib.auth.logout(request)
    return redirect('monopolowy/index')


def zamowienia(request):
    if request.user.is_authenticated:
        zamowienie = Zamowienie.objects.get(klient_id=request.user.id)
        context = {
            'zamowienia': [zamowienie],
            'logged_as_admin': request.user.is_superuser,
        }
        return render(request, 'monopolowy/zamowienia.html', context)
    else:
        context = {
            'error': 'Błąd logowania',
            'error_details': 'Nie jesteś zalogowany do konta.'
        }
        return render(request, 'monopolowy/not_logged.html', context)


def asortyment(request):
    if request.user.is_authenticated and request.user.is_superuser:
        items = Asortyment.objects.all()
        context = {
            'asortyment': items,
            'logged_as_admin': request.user.is_superuser,
        }
        return render(request, 'monopolowy/asortyment/asortyment.html', context)
    else:
        context = {
            'error': 'Błąd uprawnień',
            'error_details': 'Nie masz uprawnień dostępu do tej strony.'
        }
        return render(request, 'monopolowy/not_logged.html', context)


def asortyment_details(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        item = Asortyment.objects.get(pk=id)
        context = {
            'asortyment': item,
            'logged_as_admin': request.user.is_superuser,
        }
        return render(request, 'monopolowy/asortyment/asortyment_details.html', context)
    else:
        context = {
            'error': 'Błąd uprawnień',
            'error_details': 'Nie masz uprawnień dostępu do tej strony.'
        }
        return render(request, 'monopolowy/not_logged.html', context)

# @user_passes_test(lambda u: u.is_superuser)
class AsortymentUpdateView(UpdateView):
    model = Asortyment
    fields = [
        'nazwa',
        'typ_produktu',
        'cena',
        'opis',
        'zdjecie'
    ]
    template_name = 'monopolowy/asortyment/asortyment_edit.html'

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
