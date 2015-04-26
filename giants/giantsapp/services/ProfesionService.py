from django.db import transaction
from giantsapp.models import Mensaje, Profesion

__author__ = 'Ruben'

class ProfesionService:

    @staticmethod
    def create(character, nombre, nivel):
        profesion = Profesion()
        profesion.nombre = nombre
        profesion.nivel = nivel
        profesion.personaje = character

        return profesion

    @staticmethod
    @transaction.atomic()
    def save(profesion):
        profesion.save()