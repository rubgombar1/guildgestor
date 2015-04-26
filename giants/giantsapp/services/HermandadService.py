from giantsapp.models import Jugador, Personaje, Hermandad, Apply

__author__ = 'Ruben'


class HermandadService:

    @staticmethod
    def is_master(jugadorId, guild):
        personajes = Personaje.objects.filter(jugador__id = jugadorId)
        res = False
        if guild.master in personajes:
            res = True
        return res

    @staticmethod
    def is_member(jugadorId, guildId):
        res = False
        personajes = Personaje.objects.filter(jugador__user_account__id = jugadorId)
        for personaje in personajes:
            apply = Apply.objects.filter(personaje__id = personaje.id, hermandad__id = guildId, estado = "Aceptado")
            if apply.__len__()>0:
                res = True
                break
        return res