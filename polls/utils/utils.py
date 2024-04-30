# bingo/utils/bingo_utils.py

import random
import time

def gerar_cartela():
    cartela = []
    for letra in ['B', 'I', 'N', 'G', 'O']:
        numeros = random.sample(range(1 + (15 * 'BINGO'.index(letra)), 16 + (15 * 'BINGO'.index(letra))), 3)
        cartela.extend(numeros) 
    return cartela


def sortear_numeros():
    numeros_disponiveis = list(range(1, 76))
    numeros_sorteados = []
    while numeros_disponiveis:
        numero_sorteado = random.choice(numeros_disponiveis)
        numeros_sorteados.append(numero_sorteado)
        numeros_disponiveis.remove(numero_sorteado)
    return numeros_sorteados, numeros_disponiveis


def verificar_numero(cartela, numero_sorteado):
    for linha in cartela:
        if numero_sorteado in linha:
            return True
    return False
