# bingo/utils/bingo_utils.py

import random

def gerar_cartela():
    cartela = []
    for letra in ['B', 'I', 'N', 'G', 'O']:
        numeros = random.sample(range(1 + (15 * 'BINGO'.index(letra)), 16 + (15 * 'BINGO'.index(letra))), 3)
        cartela.extend(numeros) 
    return cartela


def sortear_numero():
    return random.list(1, 75)


def verificar_numero(cartela, numero_sorteado):
    for linha in cartela:
        if numero_sorteado in linha:
            return True
    return False
