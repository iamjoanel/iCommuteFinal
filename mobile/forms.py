import floppyforms as forms
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                               'placeholder': 'Username'}), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}), required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Invalid Username or Password")

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)

        return user
