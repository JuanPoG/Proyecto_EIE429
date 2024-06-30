from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class myUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(myUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control custom-form'})
            field.label_classes=('form-label-left', )

    
    class meta:
        model=User
        fields=("username","password1","password2")