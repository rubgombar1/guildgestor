from django.db import transaction
from giantsapp.models import Apply, Personaje, Hermandad

__author__ = 'Ruben'

class ApplyService:

    @staticmethod
    def can(apply):
        applys = Apply.objects.filter(personaje__id = apply.personaje.id, hermandad__id = apply.hermandad.id, estado = 'Aceptado')
        res = True
        if applys.__len__( )> 0:
            res = False
        return res

    @staticmethod
    def create(personajeId, guildId, jugador):
        pj = Personaje.objects.filter(id = personajeId)[0]
        pjs = Personaje.objects.filter(jugador__id = jugador.id)
        applys = Apply.objects.filter(personaje__id = personajeId, hermandad__id = guildId).exclude(estado = 'Denegada')
        apply = Apply()
        if pj in pjs and  applys.__len__()==0:
            apply.estado = 'Espera'
            apply.personaje = pj
            apply.hermandad = Hermandad.objects.filter(id = guildId)[0]
        return apply

    @staticmethod
    @transaction.atomic()
    def save(apply):
        apply.save()