import datetime
from django.db import transaction
from giantsapp.models import Evento, Hermandad


class EventoServicio:
    @staticmethod
    def createPVE(fecha,descripcion, num_tanques, num_dps, num_heal):
        evento = Evento()
        evento.fecha = fecha
        evento.descripcion = descripcion
        evento.num_tanques = num_tanques
        evento.num_dps = num_dps
        evento.tipo = 'PVE'
        evento.num_heal = num_heal
        return evento

    @staticmethod
    @transaction.atomic()
    def savePVE(event, guild):
        event.hermandad = guild
        event.save()

    @staticmethod
    def createPVP(fecha,descripcion, num):
        evento = Evento()
        evento.fecha = fecha
        evento.descripcion = descripcion
        evento.num = num
        evento.tipo = 'PVP'
        return evento

    @staticmethod
    @transaction.atomic()
    def savePVP(event, guild):
        event.hermandad = guild
        event.save()
