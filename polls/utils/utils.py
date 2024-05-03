# bingo/utils/bingo_utils.py

import random
import time

def gerar_cartela():
    cartela = {'lin1': [], 'lin2': [], 'lin3': []}
    cartela['lin1'] = sorted(random.sample(range(1, 30), 5))
    cartela['lin2'] = sorted(random.sample(range(31, 60), 5))
    cartela['lin3'] = sorted(random.sample(range(61, 90), 5))
    return cartela


def sortear_numeros():
    numeros_disponiveis = list(range(1, 91))
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
