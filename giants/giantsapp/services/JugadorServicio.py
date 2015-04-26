from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from giantsapp.forms.EditJugadorForm import EditJugadorForm
from giantsapp.models import Jugador, Personaje


class JugadorServicio:
    @staticmethod
    def object_to_form_converter(player):
        initial = {'nombre': player.nombre, 'horario': player.horario,
                   'pais': player.pais, 'edad': player.edad,
                   'experiencia':player.experiencia}

        form = EditJugadorForm()
        form.initial = initial

        return form

    @staticmethod
    @transaction.atomic()
    def form_to_object_converter(player,nombre,horario,pais,edad,experiencia):
        player.nombre=nombre
        player.horario = horario
        player.pais = pais
        player.edad = edad
        player.experiencia = experiencia
        return player

    @staticmethod
    @transaction.atomic()
    def save(jugador, userId):
        assert(jugador.user_account.id == userId, 'No puedas editar la cuenta de otro jugador')
        jugador.save()

    @staticmethod
    def create(username, password, nombre, confirm_password, horario, pais, edad, experiencia, email):
        if password != confirm_password:
            raise forms.ValidationError("Los passwords no coinciden")

        user_account = User.objects.create_user(username=username, email=email, password=password)

        jugador = Jugador(user_account = user_account, nombre=nombre, horario=horario,pais=pais, edad=edad, experiencia=experiencia)
        jugador.save()
        return jugador

    @staticmethod
    def create_pj(nickname, equipo):
        pj = Personaje()
        pj.nickname = nickname
        pj.equipo = equipo
        pj.clase = 'mago'
        pj.pve_funcion = 'p'
        pj.pvp_funcion = 'p'
        return pj

    @staticmethod
    @transaction.atomic()
    def save_pj(pj):
        pj.save()