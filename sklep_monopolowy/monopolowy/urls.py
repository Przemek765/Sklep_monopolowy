from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='monopolowy/index'),
    path('zamowienia/', zamowienia, name='monopolowy/zamowienia'),
    path('asortyment/', asortyment, name='monopolowy/asortyment'),
    path('asortyment_details/<int:id>', asortyment_details, name='monopolowy/asortyment_details'),
    path('asortyment_edit/<int:pk>', AsortymentUpdateView.as_view(), name='monopolowy/asortyment_edit'),
    path('login/', login, name='monopolowy/login'),
    path('register/', register, name='monopolowy/register'),
    path('profile/', profile, name='monopolowy/profile'),
    path('logout/', logout, name='monopolowy/logout'),
]