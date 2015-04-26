from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.core.validators import MinValueValidator
from crispy_forms.bootstrap import FormActions

__author__ = 'Ruben'


class EditJugadorForm(forms.Form):
    nombre = forms.CharField(max_length=32, label='Nombre')
    horario = forms.CharField(max_length=256, label='Horario')
    pais = forms.CharField(max_length=32, label='Pais')
    edad = forms.IntegerField(validators=[MinValueValidator(0)], label='Edad')
    experiencia = forms.CharField(widget=forms.Textarea, max_length=256, label='Experiencia')

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = 'save'
    helper.label_class = "col-sm-2"
    helper.field_class = "col-sm-10"
    helper.layout = Layout(
        Field('nombre', css_class="input-sm"),
        Field('horario', css_class="input-sm"),
        Field('pais', css_class="input-sm"),
        Field('edad', css_class="input-sm"),
        Field('experiencia', css_class="input-sm"),
        FormActions(Submit('save_edit_player', 'Enviar',css_class='btn-primary')))