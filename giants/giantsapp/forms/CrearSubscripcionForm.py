from django import forms
from giantsapp.models import Personaje
from giantsapp.services.PersonajeService import PersonajeService


class CrearSubscripcionForm(forms.Form):

    eventId = forms.CharField(max_length=256)
    personajeId = forms.ModelChoiceField(queryset=Personaje.objects.none(), to_field_name="id")

    def __init__(self,*args, **kwargs):
        guildId = kwargs.pop('eventId', -1)
        userId = kwargs.pop('userId', -1)

        super(CrearSubscripcionForm, self).__init__(*args, **kwargs)
        self.fields['eventId'].widget = forms.HiddenInput()
        self.fields['personajeId'].queryset = Personaje.objects.filter(jugador__id = userId)
        if guildId != -1:
            self.fields['eventId'].initial = guildId
