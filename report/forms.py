import floppyforms as forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': "Report Content", 'rows': '1'})
        }
