from django.db import models
from django.contrib.auth.models import User


# models.py
class Cartela(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    numeros = models.ManyToManyField('NumeroSorteado', related_name='cartelas_numeros', blank=True)
    numeros_gerados = models.JSONField()
    id_sorteio = models.ForeignKey('NumeroSorteado', related_name='cartelas_sorteio', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Cartela {self.pk} - Jogador: {self.jogador.username}"

class NumeroSorteado(models.Model):
    data_hora_sorteio = models.DateTimeField(auto_now_add=True)
    numeros = models.JSONField(default=list)
    cartela_kuadra = models.JSONField(null=True, blank=True)
    cartela_kina = models.JSONField(null=True, blank=True)
    cartela_keno = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Sorteio {self.pk} - {self.data_hora_sorteio}"

class Jogo(models.Model):
    data_inicio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Jogo {self.pk}"
