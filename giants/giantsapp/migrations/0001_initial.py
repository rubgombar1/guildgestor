# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('actor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='giantsapp.Actor')),
            ],
            options={
            },
            bases=('giantsapp.actor',),
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_apply', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.CharField(max_length=256)),
                ('num_tanques', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('num_dps', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('num_heal', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('num', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('tipo', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hermandad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=32)),
                ('descripcion', models.CharField(max_length=256)),
                ('fecha_creacion', models.DateField()),
                ('abierta', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('actor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='giantsapp.Actor')),
                ('nombre', models.CharField(max_length=32)),
                ('horario', models.CharField(max_length=256)),
                ('pais', models.CharField(max_length=32)),
                ('edad', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('experiencia', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=('giantsapp.actor',),
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asunto', models.CharField(max_length=32)),
                ('cuerpo', models.CharField(max_length=256)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('carpeta', models.CharField(max_length=32)),
                ('emisor', models.ForeignKey(related_name='emisor', to='giantsapp.Jugador')),
                ('receptor', models.ForeignKey(related_name='receptor', to='giantsapp.Jugador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=32)),
                ('clase', models.CharField(max_length=32)),
                ('pvp_funcion', models.CharField(max_length=32)),
                ('pve_funcion', models.CharField(max_length=32)),
                ('equipo', models.CharField(max_length=256)),
                ('hermandad', models.ForeignKey(to='giantsapp.Hermandad', null=True)),
                ('jugador', models.ForeignKey(related_name='personajes', to='giantsapp.Jugador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=32)),
                ('nivel', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(460)])),
                ('personaje', models.ForeignKey(related_name='+', to='giantsapp.Personaje')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscripcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('aceptado', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(related_name='+', to='giantsapp.Evento')),
                ('personaje', models.ForeignKey(related_name='+', to='giantsapp.Personaje')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hermandad',
            name='master',
            field=models.ForeignKey(related_name='master', to='giantsapp.Personaje'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evento',
            name='hermandad',
            field=models.ForeignKey(to='giantsapp.Hermandad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apply',
            name='hermandad',
            field=models.ForeignKey(related_name='applys', to='giantsapp.Hermandad'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apply',
            name='personaje',
            field=models.ForeignKey(related_name='applys', to='giantsapp.Personaje'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actor',
            name='user_account',
            field=models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
