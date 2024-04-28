from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import django.contrib.auth
from django.urls import reverse
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
    def get_kwota_zamowienia(id):
        sql = f'SELECT monopolowy_asortyment.id, SUM(monopolowy_asortyment.cena) as kwota FROM monopolowy_asortyment INNER JOIN main.monopolowy_zamowienie_asortyment mza on monopolowy_asortyment.id = mza.asortyment_id WHERE zamowienie_id = {str(id)}'
        return Zamowienie.objects.raw(sql)[0].kwota
    if request.user.is_authenticated:
        zamowienie = Zamowienie.objects.filter(klient_id=request.user.id)
        koszt_zamowienia = []
        for order in zamowienie:
            koszt_zamowienia.append(
                get_kwota_zamowienia(order.pk)
            )

        context = {
            'zamowienia': zamowienie,
            'koszt_zamowienia': koszt_zamowienia,
            'logged_as_admin': request.user.is_superuser,
        }
        return render(request, 'monopolowy/zamowienia/zamowienia.html', context)
    else:
        context = {
            'error': 'Błąd logowania',
            'error_details': 'Nie jesteś zalogowany do konta.'
        }
        return render(request, 'monopolowy/error.html', context)


def zamowienia_new(request):
    if request.user.is_authenticated:
        context = {
            'title': 'Nowe zamówienie',
            'logged_as_admin': request.user.is_superuser,
        }
        return render(request, 'monopolowy/zamowienia/new.html', context)
    else:
        context = {
            'error': 'Błąd logowania',
            'error_details': 'Nie jesteś zalogowany do konta.'
        }
        return render(request, 'monopolowy/error.html', context)


def zamowienia_delete(request, id):
    if request.user.is_authenticated:
        if Zamowienie.objects.get(klient_id=request.user.id, id=id):
            Zamowienie.objects.get(klient_id=request.user.id, id=id).delete()
            return redirect('monopolowy/zamowienia')
        else:
            context = {
                'error': 'Error 404',
                'error_details': 'Coś poszło nie tak!'
            }
            return render(request, 'monopolowy/error.html', context)
    else:
        context = {
            'error': 'Błąd logowania',
            'error_details': 'Nie jesteś zalogowany do konta.'
        }
        return render(request, 'monopolowy/error.html', context)

def zamowienia_delete_confirm(request, id):
    if request.user.is_authenticated:
        if Zamowienie.objects.get(klient_id=request.user.id, id=id):
            context = {
                'title': 'Confirm',
                'id': id
            }
            return render(request, 'monopolowy/zamowienia/confirm.html', context)
        else:
            context = {
                'error': 'Error 404',
                'error_details': 'Coś poszło nie tak!'
            }
            return render(request, 'monopolowy/error.html', context)
    else:
        context = {
            'error': 'Błąd logowania',
            'error_details': 'Nie jesteś zalogowany do konta.'
        }
        return render(request, 'monopolowy/error.html', context)

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
        return render(request, 'monopolowy/error.html', context)


def asortyment_delete(request, id):
    pass


def asortyment_delete_confirm(request, id):
    pass


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
        return render(request, 'monopolowy/error.html', context)


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

    def get_success_url(self):
        return reverse('monopolowy/asortyment_details', kwargs={'id': self.object.pk})


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
