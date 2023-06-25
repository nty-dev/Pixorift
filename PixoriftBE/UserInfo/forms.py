from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'birth_date')
        required_fields = ('username', 'displayid', 'email')

class UpdateUserForm(forms.ModelForm):
    useravatar=forms.ImageField()
    class Meta:
        model = get_user_model()
        fields = ('username', 'displayid', 'first_name', 'last_name', 'userbio', 'email', 'useravatar', 'birth_date')
