# bingo/urls.py

from django.urls import path
from .views import HomeView, JogoView, bingo_cards, signup_view, login_view, logout_view
from . import views

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('jogo/<int:jogo_id>/', JogoView.as_view(), name='jogo'),
    path('bingo-cards/', bingo_cards, name='bingo_cards'),  # Adiciona a nova view
    path('salvar_numeros_sorteados/', views.salvar_numeros_sorteados, name='salvar_numeros_sorteados'),
    # path('sorteio/', sorteio, name='sorteio')
]
