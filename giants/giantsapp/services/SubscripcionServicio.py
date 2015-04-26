from django.db import transaction
from giantsapp.models import Apply, Personaje, Hermandad, Evento, Subscripcion

__author__ = 'Ruben'

class SubscripcionServicio:
    @staticmethod
    def create(personajeId, eventId, jugador):
        pj = Personaje.objects.filter(id = personajeId)[0]
        pjs = Personaje.objects.filter(jugador__id = jugador.id)
        event = Evento.objects.filter(id= eventId)[0]
        applys = Apply.objects.filter(personaje__id = personajeId, hermandad__id = event.hermandad.id, estado = "Aceptado")
        subcription = Subscripcion()
        if pj in pjs and  applys.__len__()==1:
            subcription.personaje = pj
            subcription.evento = event
        return subcription

    @staticmethod
    @transaction.atomic()
    def save(subcription):
        subcription.save()