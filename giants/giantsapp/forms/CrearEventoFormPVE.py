from datetimewidget.widgets import DateTimeWidget
from django import forms



class CrearEventoFormPVE(forms.Form):

    guildId = forms.CharField(max_length=256)
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': 'Ej. 2016-02-10 20:00:00'}), label= 'Fecha para el evento')

    num_tanques = forms.IntegerField(min_value=0, label='Numero de tanques')
    num_dps = forms.IntegerField(min_value=0, label='Numero de DPS')
    num_heal = forms.IntegerField(min_value=0, label='Numero de sanadores')
    descripcion = forms.CharField(widget = forms.Textarea, required=True, label='Descripcion')
    def __init__(self, *args, **kwargs):
        guildId = kwargs.pop('guildId', -1)

        super(CrearEventoFormPVE, self).__init__(*args, **kwargs)
        self.fields['guildId'].widget = forms.HiddenInput()

        if guildId != -1:
            self.fields['guildId'].initial = guildId
