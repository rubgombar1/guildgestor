from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from giantsapp.models import Personaje
from giantsapp.services.PersonajeService import PersonajeService


class CrearApplyForm(forms.Form):

    guildId = forms.CharField(max_length=256)
    personajeId = forms.ModelChoiceField(queryset=Personaje.objects.none(), to_field_name="id")



    def __init__(self,*args, **kwargs):
        guildId = kwargs.pop('guildId', -1)
        userId = kwargs.pop('userId', -1)

        super(CrearApplyForm, self).__init__(*args, **kwargs)
        self.fields['guildId'].widget = forms.HiddenInput()
        self.fields['personajeId'].queryset = Personaje.objects.filter(jugador__id = userId)
        if guildId != -1:
            self.fields['guildId'].initial = guildId


    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = 'save'
    helper.label_class = "col-sm-2"
    helper.field_class = "col-sm-10"
    helper.layout = Layout(
    Field('personajeId', css_class="input-sm"),
    Field('guildId', type="hidden"),
    FormActions(Submit('create_apply', 'Enviar',css_class='btn-primary')))