from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='monopolowy/index'),
    path('zamowienia/', zamowienia, name='monopolowy/zamowienia'),
    path('zamowienia/new/', zamowienia_new, name='monopolowy/zamowienia_new'),
    path('zamowienia/delete/<int:id>/', zamowienia_delete, name='monopolowy/zamowienia_delete'),
    path('zamowienia/detail/<int:id>/confirm', zamowienia_delete_confirm, name='monopolowy/zamowienia_delete_confirm'),
    path('asortyment/', asortyment, name='monopolowy/asortyment'),
    path('asortyment/delete/<int:id>/', asortyment_delete, name='monopolowy/asortyment_delete'),
    path('asortyment/delete/<int:id>/confirm', asortyment_delete_confirm, name='monopolowy/asortyment_delete_confirm'),
    path('asortyment/details/<int:id>/', asortyment_details, name='monopolowy/asortyment_details'),
    path('asortyment/edit/<int:pk>/', AsortymentUpdateView.as_view(), name='monopolowy/asortyment_edit'),
    path('login/', login, name='monopolowy/login'),
    path('register/', register, name='monopolowy/register'),
    path('profile/', profile, name='monopolowy/profile'),
    path('logout/', logout, name='monopolowy/logout'),
]