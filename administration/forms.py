from django.forms import (Form, CharField, PasswordInput)


class AdministratorLoginForm(Form):
    username = CharField(max_length=50)
    password = CharField(widget=PasswordInput())
