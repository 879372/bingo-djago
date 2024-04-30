from django.db import models
from django.contrib.auth.models import User


class Cartela(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Vincula a cartela a um jogador
    numeros = models.ManyToManyField('NumeroSorteado', blank=True)
    numeros_gerados = models.JSONField()
    
    def __str__(self):
        return f"Cartela {self.pk} - Jogador: {self.jogador.username}"

class NumeroSorteado(models.Model):
    numeros = models.CharField(max_length=255)

    def __str__(self):
        return f"Sorteio {self.pk}" 

class Jogo(models.Model):
    data_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jogo {self.pk}"
