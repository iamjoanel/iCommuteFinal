import floppyforms as forms

from .models import Fare


valid_modes = (
    ('Jeep', 'Jeep'),
    ('Bus', 'Bus'),
)

class FareForm(forms.ModelForm):
    class Meta:
        model = Fare
        widgets = {
            'mode': forms.Select(choices=valid_modes),
            'base': forms.NumberInput(attrs={
                    'placeholder': "0.00",
                    'min': 1.00,
                    'max': 30.00,
                    'step': 0.10
                }),
            'increment': forms.NumberInput(attrs={
                    'placeholder': "0.00",
                    'min': 1.00,
                    'max': 30.00,
                    'step': 0.10
                })
        }

