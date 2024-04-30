from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Jogo, Cartela, NumeroSorteado
from .utils.utils import gerar_cartela, sortear_numeros, verificar_numero
import json

class HomeView(View):
    def get(self, request):
        return render(request, 'bingo/home.html')

class JogoView(View):
    def get(self, request, jogo_id):
        jogo = Jogo.objects.get(pk=jogo_id)
        cartelas = Cartela.objects.all()
        numeros_sorteado = NumeroSorteado.objects.filter(jogo=jogo)
        return render(request, 'bingo/jogo.html', {'jogo': jogo, 'cartelas': cartelas, 'numeros_sorteado': numeros_sorteado})

def salvar_numeros_sorteados(request):
    if request.method == 'POST':
        # Obtenha os números sorteados do corpo da solicitação POST
        numeros_sorteados = request.POST.getlist('numeros_sorteados[]')
        print(numeros_sorteados)

        # Obtenha a instância de NumeroSorteado do banco de dados
        sorteio, created = NumeroSorteado.objects.get_or_create(pk=1)

        # Carregue o JSON armazenado no banco de dados
        numeros_sorteados_json = sorteio.numeros if sorteio.numeros else '[]'
        numeros_sorteados_list = json.loads(numeros_sorteados_json)

        # Adicione o novo número à lista
        numeros_sorteados_list.extend(numeros_sorteados)

        # Transforme a lista de números em JSON
        numeros_sorteados_json_atualizado = json.dumps(numeros_sorteados_list)

        # Atualize a instância de NumeroSorteado com os números sorteados atualizados em formato JSON
        sorteio.numeros = numeros_sorteados_json_atualizado
        sorteio.save()

        # Retorne uma resposta de sucesso
        return HttpResponse('Números sorteados salvos com sucesso!', status=200)
    else:
        # Retorne uma resposta de erro se a solicitação não for do tipo POST
        return HttpResponse('Método não permitido', status=405)

@login_required
def bingo_cards(request):
    if request.method == 'POST':
        quantidade_cartelas = int(request.POST.get('quantidade_cartelas', 1))
        jogador = request.user
        # numeros_sorteados, numeros_disponiveis = sortear_numeros()
        # print(numeros_sorteados)
        # Obtém o jogador logado
        # Cria e salva as cartelas no banco de dados

        
        cartelas = []
        
        for _ in range(quantidade_cartelas):
            numeros_cartela = gerar_cartela()  # Gera os números da cartela
            numeros_gerados_str = json.dumps(numeros_cartela)  # Converte a lista de números em uma string separada por vírgulas
            nova_cartela = Cartela.objects.create(jogador=jogador, numeros_gerados=numeros_gerados_str)  # Cria a cartela com os números gerados
            cartelas.append(nova_cartela)
            
        
        for cartela in cartelas:
            cartela.numeros_gerados = str(cartela.numeros_gerados)[1:-1]
            cartela.numeros_gerados = cartela.numeros_gerados.split(',')

            print(cartela.numeros_gerados)
            

        return render(request, 'bingo/bingo_cards.html', {'cartelas': cartelas})
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