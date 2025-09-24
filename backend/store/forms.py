from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


class CustomUserChangeForm(UserChangeForm):
    password = None  # remove the password field (you don’t want to show hash)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


class CustomPasswordChangeForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ("password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"phone"}), required=True)

    address = forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"address"}), required=False)

    country= forms.CharField(widget=forms.TextInput(attrs={"class":"w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",'placeholder':"country"}),required=False)

    state= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"state"}),required=False)

    city= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"city"}),required=False)

    zip_code= forms.CharField(widget=forms.TextInput(attrs={"class":'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500','placeholder':"zip code"}),required=False)


    class Meta:
        model = Profile
        fields = ('phone', 'address', 'country', 'state', 'city', 'zip_code')
    
    def __str__(self):
        return f"{self.user.username} Profile"


