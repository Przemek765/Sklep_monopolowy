import profile

from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='monopolowy/index'),
    path('zamowienia/', zamowienia, name='monopolowy/zamowienia'),
    path('login/', login, name='monopolowy/login'),
    path('register/', register, name='monopolowy/register'),
    path('profile/', profile, name='monopolowy/profile'),
    path('logout/', logout, name='monopolowy/logout'),
]