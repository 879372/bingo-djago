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
        
        # Criar um sorteio
        sorteio = NumeroSorteado.objects.create(numeros=numeros_sorteados)
        
        cartelas = []

        for _ in range(quantidade_cartelas):
            numeros_cartela = gerar_cartela()
            numeros_gerados_str = json.dumps(numeros_cartela)
            nova_cartela = Cartela.objects.create(jogador=jogador, numeros_gerados=numeros_gerados_str, id_sorteio=sorteio)
            cartelas.append(nova_cartela)

        for cartela in cartelas:
            cartela_json = cartela.numeros_gerados
            cartela_dict = json.loads(cartela_json)
            listas_cartela = [cartela_dict['lin1'], cartela_dict['lin2'], cartela_dict['lin3']]
            numeros_sem_travessoes = [numero for lista in listas_cartela for numero in lista if isinstance(numero, int)]
            cartela.numeros_gerados = numeros_sem_travessoes

        cartela_kuadra = None
        cartela_kina = None
        cartela_keno = None
        sorteio_kuadra = None
        sorteio_kina = None
        sorteio_keno = None

        for sorteio_index, numero_sorteado in enumerate(numeros_sorteados, start=1):
            vencedores_kuadra = []
            vencedores_kina = []
            vencedores_keno = []

            for cartela_index, cartela in enumerate(cartelas):
                # Convertendo a lista plana de números de volta em linhas
                cartela_numeros = [cartela.numeros_gerados[i:i + 5] for i in range(0, len(cartela.numeros_gerados), 5)]
                
                # Verificar se alguma linha tem todos os números preenchidos
                linhas_completas = [all(numero in numeros_sorteados[:sorteio_index] for numero in linha) for linha in cartela_numeros]
                
                # Verificar se alguma linha tem pelo menos min_numeros preenchidos
                linhas_min_numeros = [sum(numero in numeros_sorteados[:sorteio_index] for numero in linha) >= 4 for linha in cartela_numeros]

                if any(linhas_completas):
                    vencedores_kina.append(cartela)

                if any(linhas_min_numeros):
                    vencedores_kuadra.append(cartela)

                if all(linhas_completas) and any(linhas_min_numeros):
                    vencedores_keno.append(cartela)

            # Se houver vencedores, verificar se há empate
            if vencedores_kuadra and cartela_kuadra is None:
                if len(vencedores_kuadra) > 1:
                    print("Houve um empate na Kuadra nas cartelas:", [cartela.pk for cartela in vencedores_kuadra])
                    cartela_kuadra = json.dumps({'tipo': 'kuadra', 'id': [c.pk for c in vencedores_kuadra], 'usuario': [c.jogador.username for c in vencedores_kuadra], 'chamada': sorteio_index, 'numeros': [c.numeros_gerados for c in vencedores_kuadra]})
                else:
                    print(f"A cartela {vencedores_kuadra[0].pk} venceu a Kuadra!")
                    cartela_kuadra = json.dumps({'tipo': 'kuadra', 'id': vencedores_kuadra[0].jogador_id , 'usuario': vencedores_kuadra[0].jogador.username , 'cartela': vencedores_kuadra[0].pk, 'chamada': sorteio_index, 'numeros': vencedores_kuadra[0].numeros_gerados})
                sorteio_kuadra = sorteio_index

            if vencedores_kina and cartela_kina is None:
                if len(vencedores_kina) > 1:
                    print("Houve um empate na Kina nas cartelas:", [cartela.pk for cartela in vencedores_kina])
                    cartela_kina = json.dumps({'tipo': 'kina', 'id': [c.pk for c in vencedores_kina], 'usuario': [c.jogador.username for c in vencedores_kina], 'chamada': sorteio_index, 'numeros': [c.numeros_gerados for c in vencedores_kina]})
                else:
                    print(f"A cartela {vencedores_kina[0].pk} venceu a Kina!")
                    cartela_kina = json.dumps({'tipo': 'kina', 'id': vencedores_kina[0].jogador_id, 'usuario': vencedores_kina[0].jogador.username, 'cartela': vencedores_kina[0].pk, 'chamada': sorteio_index, 'numeros': vencedores_kina[0].numeros_gerados})
                sorteio_kina = sorteio_index

            if vencedores_keno and cartela_keno is None:
                if len(vencedores_keno) > 1:
                    print("Houve um empate no Keno nas cartelas:", [cartela.pk for cartela in vencedores_keno])
                    cartela_keno = json.dumps({'tipo': 'keno', 'id': [c.pk for c in vencedores_keno], 'usuario': [c.jogador.username for c in vencedores_keno], 'chamada': sorteio_index, 'numeros': [c.numeros_gerados for c in vencedores_keno]})
                else:
                    print(f"A cartela {vencedores_keno[0].pk} venceu o Keno!")
                    cartela_keno = json.dumps({'tipo': 'keno', 'id': vencedores_keno[0].jogador_id, 'usuario': vencedores_keno[0].jogador.username, 'cartela': vencedores_keno[0].pk, 'chamada': sorteio_index, 'numeros': vencedores_keno[0].numeros_gerados})
                sorteio_keno = sorteio_index

            # Criar um sorteio com ou sem cartelas
            sorteio.cartela_kuadra = cartela_kuadra
            sorteio.cartela_kina = cartela_kina
            sorteio.cartela_keno = cartela_keno

            sorteio.save()
            print()
            if cartela_kuadra is not None and cartela_kina is not None and cartela_keno is not None:
                break
        
        return render(request, 'bingo/bingo_cards.html', {
            'cartelas': cartelas, 
            'numeros_sorteados': numeros_sorteados,
            'cartela_kuadra': cartela_kuadra,
            'cartela_kina': cartela_kina,
            'cartela_keno': cartela_keno,
            'sorteio_kuadra': sorteio_kuadra,
            'sorteio_kina': sorteio_kina,
            'sorteio_keno': sorteio_keno,
        })
    else:
        return render(request, 'bingo/home.html')



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