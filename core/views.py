from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from .serializers import UserSerializer, TableSerializer, PlayerSerializer

from .models import Table, Player

# Create your views here.
class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.user

        try:
            queryset = Table.objects.get(players__name__username=user)
            serializer = {'error': 'Ya estás en una mesa de juego.'}
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            player = Player.objects.get(name__username=user)
            serializer = TableSerializer(data={'players': [player]})

            if serializer.is_valid():
                table = Table()
                table.save()
                table.players.add(player)
                serializer = TableSerializer(table)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = request.user

        try:
            queryset = Table.objects.get(players__name__username=user)
            serializer = {'error': 'Ya estás en una mesa de juego.'}
            return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            player = Player.objects.get(name__username=user)
            table = Table.objects.get(id=pk)
            serializer = TableSerializer(data={'players': [player]})

            if serializer.is_valid():
                table.players.add(player)
                serializer = TableSerializer(table)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        table = Table.objects.get(id=pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def init_game(self, request, pk=None):
        table = Table.objects.get(id=pk)
        table.init_game()
        table.save()
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def set_cards(self, request, pk=None):
        table = Table.objects.get(id=pk)
        table.set_whites_card()
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def set_black(self, request, pk=None):
        table = Table.objects.get(id=pk)
        table.set_black_card()
        table.save()
        serializer = TableSerializer(table)
        return Response(serializer.data)
        


class PlayerViewsSet(viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Player.objects.get(name__username=request.user)
        serializer = PlayerSerializer(queryset)
        return Response(serializer.data)
    
    def get_table(self, request):
        user = request.user
        try:
            queryset = Table.objects.get(players__name__username=user)
            serializer = TableSerializer(queryset)
            return Response(serializer.data)

        except ObjectDoesNotExist:
            serializer={'error':'No estás en ninguna mesa de juego.'}
            return Response(serializer)
        
    def current_card(self, request, pk=0):
        queryset = Player.objects.get(name__username=request.user)
        queryset.set_current_card(pk)
        queryset.save()
        serializer = PlayerSerializer(queryset)
        return Response(serializer.data['white_cards'])

    def exit_table(self, request):
        user = request.user
        player = Player.objects.get(name__username=user)
        try:
            queryset = Table.objects.get(players__name__username=user)
            queryset.players.remove(player)
            serializer = TableSerializer(queryset)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            serializer = {'error': 'No estás en ninguna mesa de juego.'}
            return Response(serializer)
