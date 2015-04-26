# 'manage.py populatedb'
#
from datetime import date, datetime
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.contrib import auth
from giantsapp.models import *


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Borrando datos actuales...')

        auth.models.User.objects.all().delete()
        Hermandad.objects.all().delete()
        Actor.objects.all().delete()
        Admin.objects.all().delete()
        Jugador.objects.all().delete()
        Personaje.objects.all().delete()
        Profesion.objects.all().delete()
        Apply.objects.all().delete()
        Subscripcion.objects.all().delete()
        Evento.objects.all().delete()
        Mensaje.objects.all().delete()


        print('Creando cuentas de usuarios de los jugadores ...')
        jugador1_account = auth.models.User.objects.create_user(username='jugador1', email='jugador1@gmail.com',
                                                     password='jugador')
        jugador2_account = auth.models.User.objects.create_user(username='jugador2', email='jugador2@gmail.com',
                                                     password='jugador')
        jugador3_account = auth.models.User.objects.create_user(username='jugador3', email='jugador3@gmail.com',
                                                     password='jugador')
        jugador4_account = auth.models.User.objects.create_user(username='jugador4', email='jugador4@gmail.com',
                                                     password='jugador')
        print('Cuentas de usuarios de los jugadores creadas...')

        print 'Creando jugadores'
        jugador1 = Jugador(user_account = jugador1_account, nombre = "jugador1", horario = 'de 3 a 6', pais = 'es', edad = 15, experiencia = 'nada')
        jugador1.save()

        jugador2 = Jugador(user_account = jugador2_account, nombre = "jugador2", horario = 'de 3 a 6', pais = 'es', edad = 15, experiencia = 'nada')
        jugador2.save()

        jugador3 = Jugador(user_account = jugador3_account, nombre = "jugador3", horario = 'de 3 a 6', pais = 'es', edad = 15, experiencia = 'nada')
        jugador3.save()

        jugador4 = Jugador(user_account = jugador4_account, nombre = "jugador4", horario = 'de 3 a 6', pais = 'es', edad = 15, experiencia = 'nada')
        jugador4.save()
        print 'Jugadores creados'
        print 'Creando personajes'
        pj1 = Personaje(jugador  = jugador1, nickname = 'Burn', clase = 'Paladin', pvp_funcion = 'DPS_MELEE', pve_funcion = 'DPS_MELEE', equipo = 't5')
        pj1.save()
        pj2 = Personaje(jugador  = jugador1, nickname = 'Galsen', clase = 'Sacerdote', pvp_funcion = 'HEAL', pve_funcion = 'HEAL', equipo = 't5')
        pj2.save()
        pj3 = Personaje(jugador  = jugador2, nickname = 'Waengryt', clase = 'Mago', pvp_funcion = 'DPS_CASTER', pve_funcion = 'DPS_CASTER', equipo = 't5')
        pj3.save()
        pj4 = Personaje(jugador  = jugador2, nickname = 'Adler', clase = 'Druida', pvp_funcion = 'DPS_CASTER', pve_funcion = 'DPS_CASTER', equipo = 't5')
        pj4.save()
        pj5 = Personaje(jugador  = jugador3, nickname = 'Bitx', clase = 'Paladin', pvp_funcion = 'HEAL', pve_funcion = 'HEAL', equipo = 't5')
        pj5.save()
        pj6 = Personaje(jugador  = jugador3, nickname = 'Lydros', clase = 'Brujo', pvp_funcion = 'DPS_CASTER', pve_funcion = 'DPS_CASTER', equipo = 't5')
        pj6.save()
        pj7= Personaje(jugador  = jugador4, nickname = 'Flogoprofen', clase = 'Guerrero', pvp_funcion = 'TANQUE', pve_funcion = 'DPS_MELEE', equipo = 't5')
        pj7.save()
        pj8 = Personaje(jugador  = jugador4, nickname = 'Zorkiak', clase = 'Picaro', pvp_funcion = 'DPS_MELEE', pve_funcion = 'DPS_MELEE', equipo = 't5')
        pj8.save()
        pj9= Personaje(jugador  = jugador4, nickname = 'Patataonduladas', clase = 'Chaman', pvp_funcion = 'DPS_CASTER', pve_funcion = 'DPS_CASTER', equipo = 't5')

        print('Personajes creados')

        print('Creando hermandades')

        h1 = Hermandad(nombre = 'Giants', descripcion = 'Los mejores', fecha_creacion = date.today(), abierta=True, master = pj3)
        h1.save()
        h2 = Hermandad(nombre = 'Pacto Oscuro', descripcion = 'Los mejores', fecha_creacion = date.today(), master = pj7)
        h2.save()
        pj1.hermandad = h1
        pj1.save()
        pj2.hermandad = h2
        pj2.save()
        pj3.hermandad = h1
        pj3.save()
        pj5.hermandad = h2
        pj5.save()
        pj6.hermandad = h2
        pj6.save()
        pj7.hermandad = h2
        pj7.save()
        pj9.hermandad = h1
        pj9.save()
        print('Hermandades creadas')

        print('Creando profesiones')

        profesion1 = Profesion(nombre = 'Alquimia',nivel =400, personaje = pj1 )
        profesion1.save()
        profesion2 = Profesion(nombre = 'Alquimia',nivel =300, personaje = pj2 )
        profesion2.save()
        profesion3 = Profesion(nombre = 'Cocina',nivel =400, personaje = pj1 )
        profesion3.save()
        profesion4 = Profesion(nombre = 'Mineria',nivel =400, personaje = pj3 )
        profesion4.save()
        profesion5 = Profesion(nombre = 'Alquimia',nivel =400, personaje = pj5 )
        profesion5.save()
        profesion6 = Profesion(nombre = 'Joyeria',nivel =400, personaje = pj6 )
        profesion6.save()

        print('Profesiones creadas')

        print('Creando applys')

        apply1 = Apply(fecha_apply = datetime.now(), estado = 'Espera', personaje = pj8, hermandad = h1)
        apply1.save()

        print('Applys creadas')

        print('Creando evento')

        evento1 = Evento(fecha = date(2016,02,20), descripcion = 'Description', num_tanques = 2,
                         num_dps = 5, num_heal = 3, tipo = 'PVE', hermandad = h1)
        evento1.save()
        print('Eventos creados')

        print 'Creando mensajes'
        mensaje1 = Mensaje(asunto = 'Asunto de prueba1', cuerpo = 'Cuerpo de prueba1', emisor = jugador2, receptor = jugador1, carpeta = 'Salida')
        mensaje_copia_1 = Mensaje(asunto = 'Asunto de prueba1', cuerpo = 'Cuerpo de prueba1', emisor = jugador2, receptor = jugador1, carpeta = 'Entrada')
        mensaje2 = Mensaje(asunto = 'Asunto de prueba2', cuerpo = 'Cuerpo de prueba2', emisor = jugador1, receptor = jugador3, carpeta = 'Salida')
        mensaje_copia_2 = Mensaje(asunto = 'Asunto de prueba2', cuerpo = 'Cuerpo de prueba2', emisor = jugador1, receptor = jugador3, carpeta = 'Entrada')
        mensaje_copia_1.save()
        mensaje_copia_2.save()
        mensaje1.save()
        mensaje2.save()
        print 'Mensajes creados'



    def handle(self, *args, **options):
        self._migrate()
