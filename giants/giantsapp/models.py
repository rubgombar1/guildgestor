from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Actor(models.Model):
    user_account = models.ForeignKey(User, related_name='+')

class Admin(Actor):
    pass

class Jugador(Actor):
    nombre = models.CharField(max_length=32)
    horario = models.CharField(max_length=256)
    pais = models.CharField(max_length=32)
    edad = models.IntegerField(validators=[MinValueValidator(0)])
    experiencia = models.CharField(max_length=256)

class Personaje(models.Model):
    nickname = models.CharField(max_length=32)
    clase = models.CharField(max_length=32, blank=False)
    pvp_funcion = models.CharField(max_length=32)
    pve_funcion = models.CharField(max_length=32)
    equipo = models.CharField(max_length=256)

    def __str__(self):
        return self.nickname

    jugador = models.ForeignKey(Jugador, related_name='personajes')
    hermandad = models.ForeignKey('Hermandad', null=True)

class Hermandad(models.Model):
    nombre = models.CharField(max_length=32)
    descripcion = models.CharField(max_length=256)
    fecha_creacion = models.DateField()
    abierta = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    master = models.ForeignKey(Personaje, related_name='master')



class Profesion(models.Model):
    nombre = models.CharField(max_length=32)
    nivel = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(460)])

    personaje = models.ForeignKey(Personaje, related_name='+')

class Apply(models.Model):
    fecha_apply = models.DateTimeField(auto_now=False, auto_now_add=True)
    estado = models.CharField(max_length=256)

    personaje = models.ForeignKey(Personaje, related_name='applys')
    hermandad = models.ForeignKey(Hermandad, related_name='applys')


class Evento(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    descripcion = models.CharField(max_length=256)
    num_tanques = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    num_dps = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    num_heal = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    num = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    tipo = models.CharField(max_length=32)

    hermandad = models.ForeignKey('Hermandad')

class Subscripcion(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    aceptado = models.BooleanField(default=False)

    personaje = models.ForeignKey(Personaje, related_name='+')
    evento = models.ForeignKey(Evento, related_name='+')


class Mensaje(models.Model):
    asunto = models.CharField(max_length=32)
    cuerpo = models.CharField(max_length=256)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    carpeta = models.CharField(max_length=32)

    emisor = models.ForeignKey(Jugador, related_name='emisor')
    receptor = models.ForeignKey(Jugador, related_name='receptor')







