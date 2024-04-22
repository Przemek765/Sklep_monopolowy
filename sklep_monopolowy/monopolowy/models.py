from django.db import models

# Create your models here.
class Klient(models.Model):
    Imie = models.CharField(max_length=100) 
    Nazwisko = models.IntegerField() # pole liczbowe