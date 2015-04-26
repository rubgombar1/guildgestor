from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

__author__ = 'Ruben'
Profesiones = (('Alquimia','Alquimia'),('Desuello','Desuello'), ('Encantamiento', 'Encantamiento'),
               ('Herboristeria', 'Herboristeria'), ('Herreria', 'Herreria'), ('Ingenieria', 'Ingenieria'),
               ('Inscripcion', 'Inscripcion'), ('Joyeria', 'Joyeria'), ('Mineria', 'Mineria'),
               ('Peleteria', 'Peleteria'), ('Sastreria', 'Sastreria'))

class CrearProfesionForm(forms.Form):
    characterId = forms.IntegerField()
    nombre = forms.ChoiceField(required=True,label='Nombre',widget=forms.Select(), choices=Profesiones)
    nivel = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(460)], label='Nivel')

    def __init__(self, *args, **kwargs):
        characterId = kwargs.pop('characterId', -1)

        super(CrearProfesionForm, self).__init__(*args, **kwargs)
        self.fields['characterId'].widget = forms.HiddenInput()

        if characterId != -1:
            self.fields['characterId'].initial = characterId