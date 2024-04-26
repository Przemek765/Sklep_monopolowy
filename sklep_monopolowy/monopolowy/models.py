from django.conf import settings
from django.db import models


# Create your models here.
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
    zdjecie = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'Typ: {self.typ_produktu}; Nazwa: {self.nazwa}; Cena: {str(self.cena)} zł; {self.opis[:15]}...'

    class Meta:
        verbose_name_plural = "Asortyment"


class Zamowienie(models.Model):
    klient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asortyment = models.ManyToManyField(Asortyment, blank=True, related_name='asortyment')
    data = models.DateField()

    def __str__(self):
        return f'{self.klient} - {self.data}'

    class Meta:
        verbose_name_plural = "Zamówienia"
