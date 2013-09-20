import floppyforms as forms

from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        excludes = ('is_done', 'requested', )
        widgets = {
            'origin': forms.TextInput(attrs=
                  {'type': "text", 'placeholder': "Origin", 'class': 'text input', 'id': 'search-origin'}
            ),
            'destination': forms.TextInput(attrs=
            {'type': "text", 'placeholder': "Destination", 'class': 'text input', 'id': 'search-destination'}
            ),
            'count': forms.HiddenInput(),
        }


class MobileRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        excludes = ('is_done', 'requested', )
        widgets = {
            'origin': forms.TextInput(attrs=
                  {'type': "text", 'placeholder': "Origin", 'class': 'input', 'id': 'search-origin'}
            ),
            'destination': forms.TextInput(attrs=
            {'type': "text", 'placeholder': "Destination", 'class': 'input', 'id': 'search-destination'}
            ),
            'count': forms.HiddenInput(),
        }
