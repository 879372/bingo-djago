from django.db import models
from django.contrib.auth.models import User


class Cartela(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Vincula a cartela a um jogador
    numeros = models.ManyToManyField('NumeroSorteado', blank=True)
    numeros_gerados = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return f"Cartela {self.pk} - Jogador: {self.jogador.username}"

class NumeroSorteado(models.Model):
    numero = models.IntegerField(unique=True)
    cartelas = models.ManyToManyField(Cartela, related_name='numeros_sorteado')

    def __str__(self):
        return f"Número {self.numero}"

class Jogo(models.Model):
    data_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jogo {self.pk}"
