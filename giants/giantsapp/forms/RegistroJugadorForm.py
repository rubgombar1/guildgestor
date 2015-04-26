from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.core.validators import MinValueValidator


class RegistroJugadorForm(forms.Form):
    username = forms.CharField(max_length = 32, label= 'Nombre de usuario: ')
    email = forms.EmailField(max_length=64, label="Email")
    password = forms.CharField(widget = forms.PasswordInput, max_length = 32, label= 'Password')
    confirm_password = forms.CharField(widget = forms.PasswordInput, max_length = 32, label="Confirmar password")
    nombre = forms.CharField(max_length=32, label= 'Nombre', required=True)
    horario = forms.CharField(max_length=256, label= 'Horario',required=True)
    pais = forms.CharField(max_length=32, label= 'Pais',required=True)
    edad = forms.IntegerField(validators=[MinValueValidator(0)], label='Edad',required=True)
    experiencia = forms.CharField(widget=forms.Textarea, label= 'Experiencia',required=True)


    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_action = 'save'
    helper.label_class = "col-sm-2"
    helper.field_class = "col-sm-10"
    helper.layout = Layout(
        TabHolder(
            Tab('Cuenta de usuario',
                Field('username', css_class="input-sm"),
                Field('email', css_class="input-sm"),
                Field('password', css_class="input-sm"),
                Field('confirm_password', css_class="input-sm"),
                Field('nombre', css_class="input-sm"),
                Field('horario', css_class="input-sm"),
                Field('pais', css_class="input-sm"),
                Field('edad', css_class="input-sm"),
                Field('experiencia', css_class="input-sm"),)
        ),
        FormActions(Submit('save_player', 'Registrarse', css_class='btn-primary'))
    )