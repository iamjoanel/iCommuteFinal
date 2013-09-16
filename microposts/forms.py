from django import forms

from .models import Micropost

class MicropostForm(forms.ModelForm):
    content = forms.CharField(required=True, help_text="Road Reports/Status", widget=forms.widgets.Textarea(attrs={'placeholder': "Content Here", 'style': "height:80px;", 'maxlength': "200", 'id': 'content_field'}))
    class Meta:
        model = Micropost
        exclude = ('user',)

