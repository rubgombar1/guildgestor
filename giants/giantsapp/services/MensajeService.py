from django.db import transaction
from giantsapp.models import Mensaje

__author__ = 'Ruben'

class MensajeService:

    @staticmethod
    def create_send(emisor, receptor, asunto, cuerpo):
        mensaje = Mensaje()
        mensaje.emisor = emisor
        mensaje.receptor = receptor
        mensaje.asunto = asunto
        mensaje.cuerpo = cuerpo
        mensaje.carpeta = "Salida"
        return mensaje

    @staticmethod
    def create_recieve(emisor, receptor, asunto, cuerpo):
        mensaje = Mensaje()
        mensaje.emisor = emisor
        mensaje.receptor = receptor
        mensaje.asunto = asunto
        mensaje.cuerpo = cuerpo
        mensaje.carpeta = 'Entrada'
        return mensaje

    @staticmethod
    @transaction.atomic()
    def save(mensaje):
        mensaje.save()