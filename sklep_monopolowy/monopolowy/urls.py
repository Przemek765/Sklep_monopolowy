from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='monopolowy/index'),
    path('zamowienia/', zamowienia, name='monopolowy/zamowienia'),
]