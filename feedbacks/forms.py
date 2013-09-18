import floppyforms as forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('date_posted', 'approved', 'user', )
        widgets = {
            'comment': forms.Textarea(attrs={'class': "span10", 'placeholder': 'Your Feedback Here', 'id': 'feedform'}),
            'route': forms.HiddenInput()
        }

        def clean_comment(self):
            data = self.cleaned_data['comment']
            if len(data) > 140:
                raise forms.ValidationError("Comment to long!")

class FeedbackFormMobile(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('date_posted', 'approved', 'user', )
        widgets = {
            'comment': forms.Textarea(attrs={'class': "input", 'style': "height:100px;", 'placeholder': 'Your Feedback Here', 'id': 'feedform'}),
            'route': forms.HiddenInput()
        }
