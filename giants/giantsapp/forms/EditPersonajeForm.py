from django import forms
from django.core.validators import MinValueValidator

__author__ = 'Ruben'
CLASES = (('Guerrero','Guerrero'), ('Paladin','Paladin'), ('Cazador','Cazador'), ('Picaro','Picaro'), ('Sacerdote',
         'Sacerdote'), ('Caballero de la muerte','Caballero de la muerte'),('Chaman','Chaman'),
         ('Mago','Mago'), ('Brujo','Brujo'), ('Druida','Druida'))

FUNCIONES = (('DPS Caster','DPS Caster'),('DPS Melee','DPS Melee'), ('Heal', 'Heal'), ('Tanque', 'Tanque'))

class EditPersonajeForm(forms.Form):
    characterId = forms.IntegerField()
    nickname = forms.CharField(max_length=32,label='Nick', required=True)
    clase = forms.CharField(widget=forms.TextInput())
    pvp_funcion = forms.ChoiceField(required=True,label='Funcion PVP',widget=forms.Select(), choices=FUNCIONES)
    pve_funcion = forms.ChoiceField(required=True,label='Funcion PVE',widget=forms.Select(), choices=FUNCIONES)
    equipo = forms.CharField(widget=forms.Textarea)


    def __init__(self,*args, **kwargs):
        characterId = kwargs.pop('characterId', -1)
        clase = kwargs.pop('clase', -1)

        super(EditPersonajeForm, self).__init__(*args, **kwargs)
        self.fields['characterId'].widget = forms.HiddenInput()
        self.fields['clase'].initial = clase
        self.fields['clase'].widget.attrs['readonly'] = True
        if characterId != -1:
            self.fields['characterId'].initial = characterId



