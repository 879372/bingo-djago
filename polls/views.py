from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
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


class HomeView(View):
    def get(self, request):
        return render(request, 'bingo/home.html')

class JogoView(View):
    def get(self, request, jogo_id):
        jogo = Jogo.objects.get(pk=jogo_id)
        cartelas = Cartela.objects.all()
        numeros_sorteado = NumeroSorteado.objects.filter(jogo=jogo)
        return render(request, 'bingo/jogo.html', {'jogo': jogo, 'cartelas': cartelas, 'numeros_sorteado': numeros_sorteado})



# def salvar_numeros_sorteados(request):
#     if request.method == 'POST':
#         # Obtenha os números sorteados do corpo da solicitação POST
#         numeros_sorteados = request.POST.getlist('numeros_sorteados[]')

#         # Crie uma nova instância de NumeroSorteado para cada sorteio
#         sorteio = NumeroSorteado.objects.create(numeros=numeros_sorteados)

#         # Retorne uma resposta com o ID do novo sorteio criado e uma mensagem de sucesso
#         return JsonResponse({'sorteio_id': sorteio.pk, 'mensagem': 'Números sorteados salvos com sucesso!'}, status=200)
#     else:
#         # Retorne uma resposta de erro se a solicitação não for do tipo POST
#         return JsonResponse({'mensagem': 'Método não permitido'}, status=405)

@login_required
def bingo_cards(request):
    if request.method == 'POST':
        quantidade_cartelas = int(request.POST.get('quantidade_cartelas', 1))
        jogador = request.user
        numeros_sorteados, _ = sortear_numeros()  # Não precisamos dos números disponíveis aqui
        
        sorteio = NumeroSorteado.objects.create(numeros=numeros_sorteados)

        cartelas = []
        cartela_completa = None

        for _ in range(quantidade_cartelas):
            numeros_cartela = gerar_cartela()
            numeros_gerados_str = json.dumps(numeros_cartela)
            nova_cartela = Cartela.objects.create(jogador=jogador, numeros_gerados=numeros_gerados_str, id_sorteio=sorteio)
            cartelas.append(nova_cartela)

        # Verificar se alguma cartela está completa
        for cartela in cartelas:
            numeros_na_cartela = set(map(int, re.findall(r'\d+', cartela.numeros_gerados)))
            if numeros_na_cartela.issubset(numeros_sorteados):
                cartela_completa = cartela
                break

        for cartela in cartelas:
            cartela.numeros_gerados = str(cartela.numeros_gerados)[1:-1]
            cartela.numeros_gerados = cartela.numeros_gerados.split(',')

        return render(request, 'bingo/bingo_cards.html', {'cartelas': cartelas, 'cartela_completa': cartela_completa, 'numeros_sorteados': json.dumps(numeros_sorteados)})
    else:
        return render(request, 'bingo/home.html')





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