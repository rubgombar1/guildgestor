from django.conf.urls import patterns, include, url
from giantsapp.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'giants.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.index, name='index'),

    #   JUGADORES URL
    url(r'^player/player/edit$', PlayerView.edit, name='edit_player'), # EDITAR JUGADOR
    url(r'^player/player/save$', PlayerView.save_edit, name='save_edit_player'), # GUARDAR JUGADOR
    url(r'^player/create$', PlayerView.create, name='create_player'), # CREAR JUGADOR
    url(r'^player/save$', PlayerView.save, name='save_player'), # GUARDAR JUGADOR
    url(r'^player/player/show', PlayerView.show, name='show_player'), # VER PERFIL JGAODR


    #   HERMANDADES URL
    url(r'^player/guild/show', GuildView.show_guild, name='show_guild'), # VER HERMANDAD
    url(r'^player/guild/list', GuildView.list, name='list_guilds'), # VER HERMANDADES
    url(r'^player/guild/myGuilds$', GuildView.list_myGuilds, name='list_My_guilds'), # VER MIS HERMANDADES COMO MIEMBRO
    url(r'^player/guild/myGuildsMaster', GuildView.list_myGuildsMaster, name='list_My_guildsMaster'), # VER MIS HERMANDADES COMO MASTER

    #   APPLYS URL
    url(r'^player/apply/create', ApplyView.create, name='create_apply'), # CREAR APPLY COMO JUGADOR
    url(r'^player/apply/save', ApplyView.save, name='save_apply'), # GUARDAR APPLY
    url(r'^player/apply/accept', ApplyView.accept, name='accept_apply'), # ACEPTAR APPLY COMO MASTER
    url(r'^player/apply/denied', ApplyView.denied, name='denied_apply'), # BORRAR APPLY COMO JUGADOR
    url(r'^player/apply/delete', ApplyView.delete, name='delete_apply'), # BORRAR APPLY COMO JUGADOR

    #   SUBSCRIPCIONES URL
    url(r'^player/subscription/accept', SubscripcionView.accept, name='accept_subscription'),
    url(r'^player/subscription/create', SubscripcionView.create, name='create_subscripcion'),
    url(r'^player/subscription/save', SubscripcionView.save, name='save_subscripcion'),
    url(r'^player/subscription/delete', SubscripcionView.delete, name='delete_subscripcion'),

    #   PERSONAJES URL
    url(r'^player/character/edit', CharacterView.edit, name='edit_character'),
    url(r'^player/character/save_edit$', CharacterView.save_edit, name='save_edit_character'),
    url(r'^player/character/create$', CharacterView.create, name='create_character'),
    url(r'^player/character/save$', CharacterView.save, name='save_character'),
    url(r'^player/character/myCharacters$', CharacterView.list_personajes, name='list_personajes'),
    url(r'^player/character/show$', CharacterView.details, name='details_character'),

    #   MENSAJES URL
    url(r'^player/message/send$', MensajeView.send, name='send_message'),
    url(r'^player/message/delete', MensajeView.delete, name='delete_message'),
    url(r'^player/message/save$', MensajeView.save, name='save_message'),
    url(r'^player/message/sends', MensajeView.list_send_messages, name='list_send_messages'),
    url(r'^player/message/recieves', MensajeView.list_recieved_messages, name='list_recieved_messages'),
    url(r'^player/message/trash', MensajeView.list_trash_messages, name='list_trash_messages'),

    #   EVENTOS URL
    url(r'^player/event/listNextEvents', EventView.list_next_events, name='list_next_events'),
    url(r'^player/event/pvp/create$', EventView.create_pvp, name='create_pvp'),
    url(r'^player/event/pvp/save$', EventView.save_pvp, name='save_pvp'),
    url(r'^player/event/pve/create$', EventView.create_pve, name='create_pve'),
    url(r'^player/event/pve/save$', EventView.save_pve, name='save_pve'),

    #   PROFESIONES URL
    url(r'^player/profession/create$', ProfesionView.create, name='create_profession'),
    url(r'^player/profession/save$', ProfesionView.save, name='save_profession'),
    url(r'^player/profession/edit', ProfesionView.edit, name='edit_profession'),
    url(r'^player/profession/save_edit$', ProfesionView.save_edit, name='save_edit_profession'),

    # Url no encontrada
    url(r'.*', CustomErrors.error404),
)

