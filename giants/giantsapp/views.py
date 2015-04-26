import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from giantsapp.forms.CrearApplyForm import CrearApplyForm
from giantsapp.forms.CrearEventoFormPVE import CrearEventoFormPVE
from giantsapp.forms.CrearEventoFormPVP import CrearEventoFormPVP
from giantsapp.forms.CrearMensajeForm import CrearMensajeForm
from giantsapp.forms.CrearPersonajeForm import CrearPersonajeForm
from giantsapp.forms.CrearProfesionForm import CrearProfesionForm
from giantsapp.forms.CrearSubscripcionForm import CrearSubscripcionForm
from giantsapp.forms.EditJugadorForm import EditJugadorForm
from giantsapp.forms.EditPersonajeForm import EditPersonajeForm
from giantsapp.forms.EditProfesionForm import EditProfesionForm
from giantsapp.forms.RegistroJugadorForm import RegistroJugadorForm
from giantsapp.models import *
from giantsapp.services.ApplyService import ApplyService
from giantsapp.services.EventoServicio import EventoServicio
from giantsapp.services.HermandadService import HermandadService
from giantsapp.services.JugadorServicio import JugadorServicio
from giantsapp.services.MensajeService import MensajeService
from giantsapp.services.PersonajeService import PersonajeService
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from giantsapp.services.ProfesionService import ProfesionService
from giantsapp.services.SubscripcionServicio import SubscripcionServicio


class IndexView(View):
    @staticmethod
    def index(request):
        return render(request, 'index/index.html')


class PlayerView(View):
    @staticmethod
    @login_required
    def profile(request):
        jugador = Jugador.objects.filter(user_account__id=request.user.id)[0]
        personajes = Personaje.objects.filter(jugador__user_account__id=request.user.id)
        return render(request, 'jugador/perfil.html', {'jugador': jugador , 'personajes' : personajes})

    @staticmethod
    @login_required
    def show(request):
        playerId = request.GET.get('playerId')
        jugador = Jugador.objects.filter(user_account__id=playerId)[0]
        personajes = Personaje.objects.filter(jugador__user_account__id=playerId)
        return render(request, 'jugador/show.html', {'jugador': jugador , 'personajes' : personajes})


    @staticmethod
    @login_required
    def edit(request):
        jugador = Jugador.objects.filter(user_account__id=request.user.id)[0]
        if jugador.user_account.id == request.user.id:
            form = JugadorServicio.object_to_form_converter(jugador)
            return render(request,"jugador/edit.html", {'form' : form})
        else:
            raise PermissionDenied()

    @staticmethod
    def create(request):
        if request.user.is_anonymous():
            context = {
                "form" : RegistroJugadorForm()
            }
            return render(request, "jugador/create.html", context)
        else:
            raise PermissionDenied()

    @staticmethod
    def save(request):
        if request.method == "POST":
            form = RegistroJugadorForm(request.POST)
            try:
                if form.is_valid():
                    consumer = JugadorServicio.create(form.cleaned_data["username"], form.cleaned_data["password"],
                                                                form.cleaned_data["nombre"],form.cleaned_data["confirm_password"],
                                                                form.cleaned_data["horario"], form.cleaned_data["pais"],
                                                                form.cleaned_data["edad"], form.cleaned_data["experiencia"],
                                                                form.cleaned_data["email"])
                    JugadorServicio.save(consumer)
                    return redirect("/")
                else:
                    variables = {'form': form}
            except Exception as e:
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': e.message}
        else:
            return redirect('create')
        return render(request,'jugador/create.html',variables)




    @staticmethod
    @transaction.atomic()
    @login_required
    def save_edit(request):
        form = EditJugadorForm()
        if request.method == "POST":
            form = EditJugadorForm(request.POST)
            if form.is_valid():
                jugador = Jugador.objects.get(user_account=request.user)
                jugador.nombre=request.POST.get('nombre')
                jugador.horario=request.POST.get('horario')
                jugador.pais=request.POST.get('pais')
                jugador.edad=request.POST.get('edad')
                jugador.experiencia=request.POST.get('experiencia')
                JugadorServicio.save(jugador, request.user.id)
                result= redirect("/accounts/profile")

            else:
                error=form.errors
                result = render(request, "jugador/edit.html", {'form': form})

        return result

class CharacterView(View):

    @staticmethod
    @login_required
    def list_personajes(request):
        personajes_list = Personaje.objects.filter(jugador__id = request.user.id)

        paginator = Paginator(personajes_list, 5)
        page = request.GET.get('page')
        try:
            personajes = paginator.page(page)
        except PageNotAnInteger:
            personajes = paginator.page(1)
        except EmptyPage:
            personajes = paginator.page(paginator.num_pages)
        return  render(request, "character/list.html", {'personajes': personajes,'numpages' : range(1,paginator.num_pages+1)})

    @staticmethod
    @login_required()
    def details(request):
        characterId = request.GET.get('characterId')
        personaje = Personaje.objects.filter(id = characterId)[0]
        applys = list()
        profesiones = Profesion.objects.filter(personaje__id = characterId)
        if personaje.jugador.user_account.id == request.user.id:
            applys = Apply.objects.filter(personaje__id=characterId).order_by('estado')


        return render(request, 'character/details.html', {'personaje': personaje, 'userId' : request.user.id, 'applys': applys, 'profesiones' : profesiones})

    @staticmethod
    @login_required
    def create(request):
        return render(request, "character/create.html", {'form' : CrearPersonajeForm()})

    @staticmethod
    @login_required
    def save(request):
        if request.method == "POST":
            form = CrearPersonajeForm(request.POST)
            try:
                if form.is_valid():
                    jugador = Jugador.objects.get(user_account=request.user)
                    pj = PersonajeService.create(request.POST.get('nickname'), request.POST.get('clase'),
                                                     request.POST.get('pvp_funcion'), request.POST.get('pve_funcion'),
                                                     request.POST.get('equipo'))
                    pj.jugador = jugador
                    PersonajeService.save(pj, request.user.id)
                    return redirect("list_personajes")
                else:
                    variables = {'form': form}
            except Exception as e:
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': e.message}
        else:
            return redirect('create')
        return render(request,'character/create.html',variables)
    @staticmethod
    @login_required()
    def edit(request):
        characterId = request.GET.get('characterId')
        character = Personaje.objects.get(id=characterId)
        if character.jugador.user_account.id == request.user.id:
            form = PersonajeService.object_to_form_converter(character)
            return render(request,"character/edit.html", {'form' : form})
        else:
            return CustomErrors.general_error(request, 'No puede editar este personaje porque no le pertenece')

    @staticmethod
    @transaction.atomic()
    @login_required
    def save_edit(request):
        characterId = request.POST.get('characterId')
        pj = Personaje.objects.filter(id = characterId)[0]
        if pj.jugador.user_account.id == request.user.id:
            form = EditPersonajeForm(request.POST)
            if form.is_valid():
                pj.nickname = request.POST.get('nickname')
                pj.clase =request.POST.get('clase')
                pj.pvp_funcion =request.POST.get('pvp_funcion')
                pj.pve_funcion =request.POST.get('pve_funcion')
                pj.equipo =request.POST.get('equipo')

                pj.save()
                return redirect('/')
            return render(request, 'character/edit.html', {'form': form})
        else:
            return CustomErrors.general_error(request, 'No puede editar este personaje porque no le pertenece')


class ApplyView(View):

    @staticmethod
    @login_required()
    def create(request):
        guildId = request.GET.get('guildId')
        return render(request, "apply/create.html", {'form' : CrearApplyForm(guildId=guildId, userId=request.user.id)})

    @staticmethod
    @login_required()
    def save(request):
        applys = Apply.objects.filter(personaje__id = request.POST.get('personajeId')).exclude(estado='Denegado')
        if applys.__len__() == 0:
            if request.method == "POST":
                try:
                        guildId  = request.POST.get('guildId')
                        jugador = Jugador.objects.get(user_account=request.user)
                        apply = ApplyService.create(request.POST.get('personajeId'), guildId,jugador)

                        ApplyService.save(apply)
                        return redirect("list_personajes")
                except Exception as e:
                    form = CrearApplyForm(userId=request.user.id, guildId=request.POST.get('guildId'))
                    if e.message == '':
                        variables = {'form':form, 'error': e.args[1]}
                    else:
                        variables = {'form':form, 'error': 'ya tienes apply'}
            else:
                return redirect('create_apply')
            return render(request,'apply/create.html',variables)
        else:
            return CustomErrors.general_error(request, 'No puede echar un apply en esta hermandad debido a que ya tienes un apply activa')

    @staticmethod
    @login_required()
    def delete(request):
        applyId = request.GET.get('applyId')
        apply = Apply.objects.filter(id = applyId)[0]
        if apply.personaje.jugador.user_account.id == request.user.id:
            apply.delete()
            return redirect('/player/character/show?characterId='+str(apply.personaje.id))
        else:
            return CustomErrors.general_error(request, 'No puede borrar este apply porque no le pertenece')

    @staticmethod
    @login_required()
    def denied(request):

        applyId = request.GET.get('applyId')
        apply = Apply.objects.filter(id = applyId)[0]
        if apply.hermandad.master.jugador.user_account.id == request.user.id:
            apply.estado = 'Denegado'
            PersonajeService.update_guild(apply)
            apply.save()
            return redirect('/player/guild/show?guildId='+str(apply.hermandad.id))
        else:
            return CustomErrors.general_error(request, 'No puede denegar este apply porque no es el maestro de hermandad')



    @staticmethod
    @login_required()
    def accept(request):
        applyId = request.GET.get('applyId')
        apply = Apply.objects.filter(id = applyId)[0]
        #TODO Controlar las cositas
        can = ApplyService.can(apply)
        if can:
            apply.estado = 'Aceptado'
            apply.save()
            PersonajeService.update_guild(apply)
            return redirect('/player/guild/show?guildId='+str(apply.hermandad.id))
        else:
            return CustomErrors.general_error(request, 'No puede aceptar este apply para ese personaje')




class EventView(View):

    @staticmethod
    def create_pve(request):
        id = request.GET.get('guildId')
        guild = Hermandad.objects.filter(id=id)[0]
        if guild.master.jugador.user_account.id == request.user.id:
            return render(request, "event/create.html", {'form' : CrearEventoFormPVE(guildId = id)})
        else:
            return CustomErrors.general_error(request, 'No puede crear evento si no es el guild master')

    @staticmethod
    def save_pve(request):
        if request.method == "POST":
            form = CrearEventoFormPVE(request.POST)
            try:
                if form.is_valid():
                    event = EventoServicio.createPVE(request.POST.get('fecha'),request.POST.get('descripcion'), request.POST.get('num_tanques'),
                                                     request.POST.get('num_dps'),request.POST.get('num_heal'))
                    guild = Hermandad.objects.filter(id = request.POST.get('guildId'))[0]
                    if guild.master.jugador.user_account.id == request.user.id:
                        EventoServicio.savePVE(event, guild)
                    else:
                        return CustomErrors.general_error(request, 'No puede crear evento si no es el guild master')


                    return redirect("/player/guild/show?guildId='+request.POST.get('guildId")
                else:
                    variables = {'form': form}
            except Exception as e:
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': e.message}
        else:
            return redirect('/player/guild/show?guildId='+request.POST.get('guildId'))
        return render(request,'event/create.html',variables)

    @staticmethod
    def create_pvp(request):
        id = request.GET.get('guildId')
        guild = Hermandad.objects.filter(id=id)[0]
        if guild.master.jugador.user_account.id == request.user.id:
            return render(request, "event/create.html", {'form' : CrearEventoFormPVP(guildId = id)})
        else:
            return CustomErrors.general_error(request, 'No puede crear evento si no es el guild master')

    @staticmethod
    def save_pvp(request):
        if request.method == "POST":
            form = CrearEventoFormPVP(request.POST)
            try:
                if form.is_valid():
                    event = EventoServicio.createPVP(request.POST.get('fecha'),request.POST.get('descripcion'), request.POST.get('num'))
                    guild = Hermandad.objects.filter(id = request.POST.get('guildId'))[0]

                    if guild.master.jugador.user_account.id == request.user.id:
                        EventoServicio.savePVP(event, guild)
                    else:
                        return CustomErrors.general_error(request, 'No puede crear evento si no es el guild master')
                    return redirect('/player/guild/show?guildId='+request.POST.get('guildId'))
                else:
                    variables = {'form': form}
            except Exception as e:
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': e.message}
        else:
            return redirect('/')
        return render(request,'event/create.html',variables)

    @staticmethod
    @login_required()
    def list_next_events(request):
        guildId = request.GET.get('guildId')
        userId = request.user.id
        guild = Hermandad.objects.filter(id = guildId)[0]
        is_member = HermandadService.is_member(jugadorId=userId, guildId=guildId)
        is_master = HermandadService.is_master(jugadorId=userId, guild=guild)
        events_list = None
        events = None
        if is_master or is_member:
            events_list = Evento.objects.filter(hermandad__id = guildId, fecha__gte = datetime.datetime.now()).order_by('fecha')
        if events_list != None and events_list.__len__() > 0:
            paginator = Paginator(events_list,5)
            page = request.GET.get('page')
            try:
                events = paginator.page(page)
            except PageNotAnInteger:
                    events = paginator.page(1)
            except EmptyPage:
                events = paginator.page(paginator.num_pages)
        if events == None:
            return redirect('/')
        return render(request, "event/list.html", {'events' : events})

class GuildView(View):

    @staticmethod
    def list(request):
        guilds_list = Hermandad.objects.all()
        paginator = Paginator(guilds_list, 5)
        page = request.GET.get('page')
        try:
            guilds = paginator.page(page)
        except PageNotAnInteger:
            guilds = paginator.page(1)
        except EmptyPage:
            guilds = paginator.page(paginator.num_pages)
        return  render(request, "guild/list.html", {'guilds': guilds,'numpages' : range(1,paginator.num_pages+1)})

    @staticmethod
    @login_required()
    def list_myGuilds(request):
        guilds_list = PersonajeService.list_my_guilds(request.user.id)
        guilds=list()
        paginator = Paginator(guilds_list, 5)
        if guilds_list.__len__() > 0:
            page = request.GET.get('page')
            try:
                guilds = paginator.page(page)
            except PageNotAnInteger:
                guilds = paginator.page(1)
            except EmptyPage:
                guilds = paginator.page(paginator.num_pages)
        return  render(request, "guild/list.html", {'guilds': guilds,'numpages' : range(1,paginator.num_pages+1)})

    @staticmethod
    @login_required()
    def list_myGuildsMaster(request):
        guilds_list = Hermandad.objects.filter(master__jugador__user_account__id = request.user.id)
        guilds = list()
        paginator = Paginator(guilds_list, 5)
        if guilds_list.__len__() > 0:
            page = request.GET.get('page')
            try:
                guilds = paginator.page(page)
            except PageNotAnInteger:
                guilds = paginator.page(1)
            except EmptyPage:
                guilds = paginator.page(paginator.num_pages)
        return  render(request, "guild/list.html", {'guilds': guilds,'numpages' : range(1,paginator.num_pages+1)})

    @staticmethod
    def show_guild(request):
        guildId = request.GET.get('guildId')
        guild = Hermandad.objects.filter(id = guildId)[0]
        is_master = HermandadService.is_master(jugadorId=request.user.id, guild=guild)
        applys = list()
        if is_master:
            applys_list = Apply.objects.filter(hermandad__id = guildId, estado = 'Espera')
            paginator = Paginator(applys_list, 5)
            page = request.GET.get('page')
            try:
                applys = paginator.page(page)
            except PageNotAnInteger:
                applys = paginator.page(1)
            except EmptyPage:
                applys = paginator.page(paginator.num_pages)
        return render(request, "guild/show.html", {'guild' : guild, 'is_master' : is_master, 'applys' : applys, 'userId' : request.user.id})

class SubscripcionView(View):

    @staticmethod
    @login_required()
    def create(request):
        eventId = request.GET.get('eventId')
        subs = Subscripcion.objects.filter(personaje__usuario__user_account__id = request.user.id, event__id = eventId)
        if subs.__len__()!= 0:
            return render(request, "subscription/create.html", {'form' : CrearSubscripcionForm(eventId=eventId, userId=request.user.id)})
        else:
            return CustomErrors.general_error(request, 'No puedes realizar mas de una subscripcion a un evento')
    @staticmethod
    @login_required()
    def save(request):
        if request.method == "POST":
            try:
                    jugador = Jugador.objects.get(user_account=request.user)
                    subscription = SubscripcionServicio.create(request.POST.get('personajeId'), request.POST.get('eventId'),jugador)
                    event = Evento.objects.filter(id = request.POST.get('eventId'))[0]
                    subs = Subscripcion.objects.filter(personaje__usuario__user_account__id = request.user.id, event__id = request.POST.get('eventId'))
                    applys = Apply(personaje__id = request.POST.get('personajeId'), hermandad__id = event.hermandad.id, estado = "Aceptado")
                    if subs.__len__() != 0:
                        if applys != 1:
                            SubscripcionServicio.save(subscription)
                        else:
                            return CustomErrors.general_error(request, 'No puede realizar una subscripcion para el evento si no pertenece a la hermandad')
                    else:
                            return CustomErrors.general_error(request, 'No puede realizar una subscripcion para el evento si ya tiene alguna')
                    return redirect("/player/event/show?eventId="+request.POST.get('eventId'))
            except Exception as e:
                form = CrearSubscripcionForm(userId=request.user.id, eventId=request.POST.get('eventId'))
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': 'ya tienes subscripcion'}
        else:
            return redirect('create')
        return render(request,'character/create.html',variables)

    @staticmethod
    @login_required()
    def delete(request):
        subscriptionId = request.GET.get('subscriptionId')
        subcription = Subscripcion.objects.filter(id = subscriptionId)[0]
        if subcription.personaje.jugador.id == request.user.id:
            subcription.delete()
        return redirect('/player/character/show?characterId='+str(subcription.personaje.id))

    @staticmethod
    @login_required()
    def accept(request):
        subscriptionId = request.GET.get('subscriptionId')
        subscription = Subscripcion.objects.filter(id = subscriptionId)[0]
        #TODO Controlar las cositas
        subscription.aceptado = 1
        subscription.save()
        return redirect('/')

class MensajeView(View):

    @staticmethod
    @login_required()
    def list_send_messages(request):
        messageId = request.GET.get('messageId')
        messages  = Mensaje.objects.filter(emisor__id = request.user.id, carpeta = 'Salida')
        message = None
        if not messageId == None:
            message = Mensaje.objects.filter(id = messageId)[0]
        return render(request,'message/list.html',{'messages' : messages, 'tipo' : 'sends','lista':'enviados', 'message' : message})

    @staticmethod
    @login_required()
    def list_recieved_messages(request):
        messageId = request.GET.get('messageId')
        messages  = Mensaje.objects.filter(receptor__id = request.user.id, carpeta = 'Entrada')
        message = None
        if not messageId == None:
            message = Mensaje.objects.filter(id = messageId)[0]
        return render(request,'message/list.html',{'messages' : messages, 'tipo' : 'trash','lista':'recibidos', 'message' : message})

    @staticmethod
    @login_required()
    def list_trash_messages(request):
        messageId = request.GET.get('messageId')
        messages  = Mensaje.objects.filter(receptor__id = request.user.id, carpeta = 'Papelera')
        message = None
        if not messageId == None:
            message = Mensaje.objects.filter(id = messageId)[0]
        return render(request,'message/list.html',{'messages' : messages, 'tipo' : 'recieves','lista':'eliminados', 'message' : message})

    @staticmethod
    @login_required()
    def send(request):
        receivedId = request.GET.get('receivedId')
        return render(request, 'message/create.html', {'form' : CrearMensajeForm(receivedId=receivedId)})

    @staticmethod
    @login_required()
    def save(request):
        if request.method == "POST":
            try:
                    emisor = Jugador.objects.get(user_account=request.user)
                    receptor = Jugador.objects.get(user_account__id = request.POST.get('receivedId'))
                    mensaje1 = MensajeService.create_send(emisor, receptor, request.POST.get('asunto'), request.POST.get('cuerpo'))
                    mensaje2 = MensajeService.create_recieve(emisor, receptor, request.POST.get('asunto'), request.POST.get('cuerpo'))

                    MensajeService.save(mensaje1)
                    MensajeService.save(mensaje2)

                    return redirect("/accounts/profile")
            except Exception as e:
                form = CrearMensajeForm(recievedId=request.POST.get('receivedId'))
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': e}
        else:
            return redirect('create')
        return render(request,'message/create.html',variables)

    @staticmethod
    def delete(request):
        messageId = request.GET.get('messageId')

        message = Mensaje.objects.filter(id = messageId)[0]
        if message.carpeta == 'Entrada':
            message.carpeta = 'Papelera'
            message.save()
        else:
            message.delete()
        return redirect('/player/message/' + request.GET.get('type'))

class ProfesionView(View):

    @staticmethod
    @login_required()
    def create(request):
        characterId = request.GET.get('characterId')
        return render(request, 'profession/create.html', {'form' : CrearProfesionForm(characterId=characterId)})


    @staticmethod
    @login_required()
    def save(request):
        if request.method == "POST":
            try:
                    character = Personaje.objects.get(id=request.POST.get('characterId'))

                    profesion = ProfesionService.create(character, request.POST.get('nombre'), request.POST.get('nivel'))
                    profesiondb = Profesion.objects.filter(personaje = character, nombre = request.POST.get('nombre'))
                    if profesiondb.__len__() == 0:
                        MensajeService.save(profesion)
                    else:
                        return CustomErrors.general_error(request, 'Este personaje ya tiene asignada esa profesion, por lo tanto no puedes crearla, sino modificarla')
                    return redirect('/player/character/show?characterId=' + request.POST.get('characterId'))
            except Exception as e:
                form = CrearProfesionForm(characterId=request.POST.get('characterId'))
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': 'ya tienes subscripcion'}
        else:
            return redirect('create')
        return render(request,'profession/create.html',variables)

    @staticmethod
    @login_required()
    def edit(request):
        professionId = request.GET.get('professionId')
        return render(request, 'profession/edit.html', {'form' : EditProfesionForm(professionId=professionId)})


    @staticmethod
    @login_required()
    def save_edit(request):
        if request.method == "POST":
            try:
                    professionId = request.POST.get('professionId')

                    profesion = Profesion.objects.filter(id=professionId)[0]
                    profesion.nivel = request.POST.get('nivel')

                    ProfesionService.save(profesion)
                    return redirect("/player/character/show?characterId=" + str(profesion.personaje.id))
            except Exception as e:
                form = EditProfesionForm(request.POST.get('professionId'))
                if e.message == '':
                    variables = {'form':form, 'error': e.args[1]}
                else:
                    variables = {'form':form, 'error': 'ya tienes subscripcion'}
        else:
            return redirect('create')
        return render(request,'profession/edit.html',variables)

class CustomErrors(View):

    @staticmethod
    def error404(request):
        error = "(404) Recurso no encontrado"
        return render(request,'errors/variable_error.html', {'error' : error})

    @staticmethod
    def error403(request):
        error = "(403) Permiso denegado"
        return render(request,'errors/variable_error.html', {'error' : error})

    @staticmethod
    def general_error(request, error):
        return render(request, 'errors/general_error.html', {'error' : error})