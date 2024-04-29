from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Jogo, Cartela, NumeroSorteado
from .utils.utils import gerar_cartela, sortear_numero, verificar_numero

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
        jogador = request.user  # Obtém o jogador logado

        # Cria e salva as cartelas no banco de dados
        cartelas = []
        for _ in range(quantidade_cartelas):
            numeros_cartela = gerar_cartela()  # Gera os números da cartela
            numeros_gerados_str = ','.join(map(str, numeros_cartela))  # Converte a lista de números em uma string separada por vírgulas
            nova_cartela = Cartela.objects.create(jogador=jogador, numeros_gerados=numeros_gerados_str)  # Cria a cartela com os números gerados
            cartelas.append(nova_cartela)
            
        # Dividir a string de números gerados em uma lista para cada cartela
        for cartela in cartelas:
            cartela.numeros_gerados = cartela.numeros_gerados.split(',')

        return render(request, 'bingo/bingo_cards.html', {'cartelas': cartelas})
    else:
        return render(request, 'bingo/home.html')


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