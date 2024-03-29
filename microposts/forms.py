import floppyforms as forms

from .models import Micropost

class MicropostForm(forms.ModelForm):
    content = forms.CharField(required=True, help_text="Road Reports/Status", widget=forms.widgets.Textarea(attrs={'placeholder': "Report Road Status", 'style': "height:80px;", 'maxlength': "200", 'id': 'content_field'}))
    class Meta:
        model = Micropost
        exclude = ('user',)


class MobileForm(forms.ModelForm):
    content = forms.CharField(required=True, help_text="Road Reports/Status", widget=forms.widgets.Textarea(attrs={'placeholder': "Report Road Status", 'maxlength': "200", 'class': 'input', 'style': "height:100px;"}))
    class Meta:
        model = Micropost
        exclude = ('user',)

