import floppyforms as forms

from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        excludes = ('is_done', 'requested', )
        widgets = {
            'origin': forms.TextInput(attrs=
                  {'type': "text", 'placeholder': "Origin", 'class': 'text input'}
            ),
            'destination': forms.TextInput(attrs=
            {'type': "text", 'placeholder': "Destination", 'class': 'text input'}
            ),
            'count': forms.HiddenInput(),
        }
