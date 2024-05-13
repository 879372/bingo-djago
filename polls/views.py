from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Jogo, Cartela, NumeroSorteado
from .utils.utils import gerar_cartela, sortear_numeros, verificar_numero
import json
from django.http import JsonResponse
from django.db.models import Count
import re
from django.core.exceptions import ObjectDoesNotExist



class HomeView(View):
    def get(self, request):
        return render(request, 'bingo/home.html')

class JogoView(View):
    def get(self, request, jogo_id):
        jogo = Jogo.objects.get(pk=jogo_id)
        cartelas = Cartela.objects.all()
        numeros_sorteado = NumeroSorteado.objects.filter(jogo=jogo)
        return render(request, 'bingo/jogo.html', {'jogo': jogo, 'cartelas': cartelas, 'numeros_sorteado': numeros_sorteado})


@login_required
def bingo_cards(request):
    if request.method == 'POST':
        quantidade_cartelas = int(request.POST.get('quantidade_cartelas', 1))
        jogador = request.user
        numeros_sorteados, _ = sortear_numeros()  # Não precisamos dos números disponíveis aqui
        
        sorteio = NumeroSorteado.objects.create(numeros=numeros_sorteados)
        cartelas = []

        # Variáveis para armazenar informações sobre as cartelas vencedoras
        primeira_cartela_linhas_completas = None
        primeira_cartela_linhas_min_numeros = None
        primeira_cartela_cartela_completa = None

        for _ in range(quantidade_cartelas):
            numeros_cartela = gerar_cartela()
            numeros_gerados_str = json.dumps(numeros_cartela)
            nova_cartela = Cartela.objects.create(jogador=jogador, numeros_gerados=numeros_gerados_str, id_sorteio=sorteio)
            cartelas.append(nova_cartela)

        for cartela in cartelas:
            cartela_json = cartela.numeros_gerados
            cartela_dict = json.loads(cartela_json)
            lista_col1 = cartela_dict['lin1']
            lista_col2 = cartela_dict['lin2']
            lista_col3 = cartela_dict['lin3']
            todas_listas = [lista_col1, lista_col2, lista_col3]
            numeros_sem_travessoes = []

            linhas_completas = any(all(numero in numeros_sorteados for numero in linha) for linha in todas_listas)
            linhas_min_numeros = any(sum(numero in numeros_sorteados for numero in linha) >= 4 for linha in todas_listas)
            cartela_completa = all(numero in numeros_sorteados for linha in todas_listas for numero in linha)

            for lista in todas_listas:
                numeros_sem_travessoes.extend([numero for numero in lista if isinstance(numero, int)])
            cartela.numeros_gerados = numeros_sem_travessoes
            cartela.numeros_gerados = str(cartela.numeros_gerados)[1:-1]
            cartela.numeros_gerados = cartela.numeros_gerados.split(',')

            # Lógica para verificar a primeira cartela a alcançar cada estado vencedor
            if linhas_completas and primeira_cartela_linhas_completas is None:
                primeira_cartela_linhas_completas = cartela
            if linhas_min_numeros and primeira_cartela_linhas_min_numeros is None:
                primeira_cartela_linhas_min_numeros = cartela
            if cartela_completa and primeira_cartela_cartela_completa is None:
                primeira_cartela_cartela_completa = cartela
            
            print(todas_listas)
            print(primeira_cartela_linhas_completas, '1')
            print(primeira_cartela_linhas_min_numeros, '2')
            print(primeira_cartela_cartela_completa, '3')
        return render(request, 'bingo/bingo_cards.html', {'cartelas': cartelas, 'primeira_cartela_linhas_completas': primeira_cartela_linhas_completas, 'primeira_cartela_linhas_min_numeros': primeira_cartela_linhas_min_numeros, 'primeira_cartela_cartela_completa': primeira_cartela_cartela_completa, 'numeros_sorteados': numeros_sorteados})
    else:
        return render(request, 'bingo/home.html')



def verificar_estado_cartela(cartela, numeros_sorteados, min_numeros):
        linhas_completas = any(all(numero in numeros_sorteados for numero in linha) for linha in cartela.numeros_gerados.values())
        linhas_min_numeros = any(sum(numero in numeros_sorteados for numero in linha) >= 4 for linha in cartela.numeros_gerados.values())
        cartela_completa = all(numero in numeros_sorteados for linha in cartela.numeros_gerados.values() for numero in linha)
        print(linhas_completas)
        print(linhas_min_numeros)
        print(cartela_completa)
        return linhas_completas, linhas_min_numeros, cartela_completa



def salvar_numeros_sorteados(request):
    ultimo_sorteio = NumeroSorteado.objects.latest('id')
    cartelas_do_sorteio = Cartela.objects.filter(id_sorteio_id=ultimo_sorteio.id)
        # Iterar sobre as cartelas encontradas
    for cartela in cartelas_do_sorteio:
        numeros_gerados = cartela.numeros_gerados
        print(numeros_gerados)  

    sorteio = NumeroSorteado.objects.get(id=ultimo_sorteio.id)
    print(sorteio.numeros)

    return render(request, 'bingo/bingo_cards.html', {'message': 'Nenhum jogador teve todos os números da cartela sorteados.'})



def sorteio(request):
    numeros_sorteados, numeros_disponiveis = sortear_numeros()
    print(numeros_disponiveis)
    print(numeros_sorteados)
    return render(request, 'bingo/sorteio.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('bingo_cards')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # Redireciona para a view 'bingo_cards'
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')