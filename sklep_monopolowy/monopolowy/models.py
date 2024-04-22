from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

# Create your models here.
class Klient(models.Model):
    imie = models.CharField(max_length=100) 
    nazwisko = models.CharField(max_length=100) 
    wiek = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    adres = models.CharField(max_length=1000)

class Asortyment(models.Model):
    typ_choice = [
        ('szlugi', 'Papierosy'),
        ('jednorazowki', 'E-papierosy jednorazowe'),
        ('alkohol lekki', 'Alkohole niski voltage'),
        ('alkohol gruby', 'Alkohole wysoki voltage'),
    ]
    nazwa = models.CharField(max_length=100)
    typ_produktu = models.CharField(max_length=100, choices=typ_choice)
    cena = models.DecimalField(max_digits=7, decimal_places=2)
    opis = models.TextField(max_length=1000)

class Zamowienia(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    asortyment = models.ForeignKey(Asortyment, on_delete=models.CASCADE)
    data = models.DateField()





