from django.db import transaction
from giantsapp.forms.EditPersonajeForm import EditPersonajeForm
from giantsapp.models import Personaje



class PersonajeService:

    @staticmethod
    def update_guild(apply):
        personaje = Personaje.objects.filter(id = apply.personaje.id)[0]
        if apply.estado == 'Aceptado':
            personaje.hermandad = apply.hermandad
        elif apply.estado == 'Denegado':
            personaje.hermandad = None
        personaje.save()


    @staticmethod
    def list_my_guilds(jugadorId):
        personajes = Personaje.objects.filter(jugador__user_account__id = jugadorId)
        res = list()
        for personaje in personajes:
            if personaje.hermandad != None:
                res.append(personaje.hermandad)
        return res

    @staticmethod
    def create(nickname,clase,pve_funcion, pvp_funcion, equipo):
        pj = Personaje()
        pj.nickname = nickname
        pj.equipo = equipo
        pj.clase = clase
        pj.pve_funcion = pve_funcion
        pj.pvp_funcion = pvp_funcion
        return pj

    @staticmethod
    @transaction.atomic()
    def save(pj, userId):
        assert pj.jugador.user_account.id == userId
        pj.save()

    @staticmethod
    def PERSONAJES(userId):
        personajes = Personaje.objects.filter(jugador__id = userId)
        PERSONAJES = list()
        for pj in personajes:
            aux = (pj.nickname, pj.id)
            PERSONAJES.append(aux)
        return PERSONAJES
    @staticmethod
    def object_to_form_converter(personaje):
        initial = {'nickname': personaje.nickname,
                   'equipo':personaje.equipo,
                   'characterId' : personaje.id, 'clase' : personaje.clase}

        form = EditPersonajeForm()
        form.initial = initial

        return form