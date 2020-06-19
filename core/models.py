from django.db import models
from django.contrib.auth.models import User

from rest_framework import serializers

from . import utils
import json
import ast

# Create your models here.
class Player(models.Model):
    name = models.OneToOneField(User, verbose_name='Nombre', on_delete=models.CASCADE, primary_key=True)
    current_card = models.CharField(max_length=999, verbose_name='Carta Actual', blank=True, null=True)
    white_cards = utils.ListField(verbose_name='Cartas Blancas', blank=True, null=True)

    def set_white_cards(self):
        cards = []
        for _ in range(9+1):
            card = utils.get('/answer')
            cards.append(card)
        self.white_cards = cards

    def set_current_card(self, index):
        index = int(index)
        self.current_card = self.white_cards[index]
        del self.white_cards[index]

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

    def __str__(self):
        return self.name.username

class Table(models.Model):
    id = models.CharField(max_length=6, verbose_name="Código",
                          primary_key=True, default=utils.id_generator())
    players = models.ManyToManyField(
        Player, verbose_name="Jugadores", blank=True)
    black_card = models.CharField(
        max_length=999, verbose_name='Carta Negra', blank=True, null=True)
    is_active = models.BooleanField(verbose_name="Juego Iniciado", default=False)

    def set_black_card(self):
        card = utils.get('/question')
        self.black_card = card

    def init_game(self):
        self.set_black_card()
        self.is_active = True
        for player in self.players.all():
            player.set_white_cards()
            player.current_card = None
            player.save()

    def set_whites_card(self):
        for player in self.players.all():
            player.set_white_cards()
            player.current_card = None
            player.save()

    class Meta:
        verbose_name = "Tabla de Juego"
        verbose_name_plural = "Tablas de Juego"
    
    def __str__(self):
        return self.id
