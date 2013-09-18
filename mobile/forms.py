import floppyforms as forms
from django.contrib import auth


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'placeholder': "Username", 'id': "origin", 'name': "origin", 'class': "text input"}), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': "text", 'placeholder': "Password", 'id': "destination", 'name': "destination", 'class': "text input"}), required=True)

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


class SearchForm(forms.Form):
    origin = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'placeholder': "Origin", 'id': "origin", 'name': "origin", 'class': "text input"}))
    destination = forms.CharField(widget=forms.TextInput(attrs={'type': "text", 'placeholder': "Destination", 'id': "destination", 'name': "destination", 'class': "text input"}))

    def cleaned_origin(self):
        if self.cleaned_data['origin'] is None:
            raise forms.ValidationError("Some fields were left blank.")
        return self.cleaned_data['origin']

    def cleaned_destination(self):
        if self.cleaned_data['destination'] is None:
            raise forms.ValidationError("Some fields were left blank.")
        return self.cleaned_data['destination']
