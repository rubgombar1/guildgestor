from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms

CLASES = (('',''),('Guerrero','Guerrero'), ('Paladin','Paladin'), ('Cazador','Cazador'), ('Picaro','Picaro'), ('Sacerdote',
         'Sacerdote'), ('Caballero de la muerte','Caballero de la muerte'),('Chaman','Chaman'),
         ('Mago','Mago'), ('Brujo','Brujo'), ('Druida','Druida'))

FUNCIONES = (('',''),('DPS Caster','DPS Caster'),('DPS Melee','DPS Melee'), ('Heal', 'Heal'), ('Tanque', 'Tanque'))

class CrearPersonajeForm(forms.Form):
    nickname = forms.CharField(max_length=32,label='Nickname', required=True)
    clase = forms.ChoiceField(required=True,label='Clase',widget=forms.Select(), choices=CLASES)
    pvp_funcion = forms.ChoiceField(required=True,label='Funcion PVP',widget=forms.Select(), choices=FUNCIONES)
    pve_funcion = forms.ChoiceField(required=True,label='Funcion PVE',widget=forms.Select(), choices=FUNCIONES)
    equipo = forms.CharField(widget=forms.Textarea)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = 'save'
    helper.label_class = "col-sm-2"
    helper.field_class = "col-sm-10"
    helper.layout = Layout(
        Field('nickname', css_class="input-sm"),
        Field('clase', css_class="input-sm"),
        Field('pvp_funcion', css_class="input-sm"),
        Field('pve_funcion', css_class="input-sm"),
        Field('equipo', css_class="input-sm"),
    FormActions(Submit('save_character', 'Crear Personaje', css_class='btn-primary')))





