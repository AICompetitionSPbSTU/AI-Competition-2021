from django import forms
from botArena.models import Bot, Game


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('url_source', 'game', 'creator_name',)


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'source')