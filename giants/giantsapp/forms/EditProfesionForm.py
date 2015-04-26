from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

__author__ = 'Ruben'


class EditProfesionForm(forms.Form):
    professionId = forms.IntegerField()
    nivel = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(460)], label='Nivel')

    def __init__(self, *args, **kwargs):
        professionId = kwargs.pop('professionId', -1)

        super(EditProfesionForm, self).__init__(*args, **kwargs)
        self.fields['professionId'].widget = forms.HiddenInput()

        if professionId != -1:
            self.fields['professionId'].initial = professionId