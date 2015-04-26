from django import forms

__author__ = 'Ruben'

class CrearMensajeForm(forms.Form):
    receivedId = forms.IntegerField()
    asunto = forms.CharField(widget=forms.TextInput, required=True, label='Asunto')
    cuerpo = forms.CharField(widget = forms.Textarea, required=True, label='Cuerpo del mensaje')

    def __init__(self, *args, **kwargs):
        receivedId = kwargs.pop('receivedId', -1)

        super(CrearMensajeForm, self).__init__(*args, **kwargs)
        self.fields['receivedId'].widget = forms.HiddenInput()

        if receivedId != -1:
            self.fields['receivedId'].initial = receivedId