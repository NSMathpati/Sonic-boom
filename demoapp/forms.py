from django import forms
from django.contrib.auth.models import User
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django import forms
from django.contrib.auth.models import User


from .models import Album, Song
# from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo','is_private']

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['is_private'].label = "Is this a private album ?"

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']