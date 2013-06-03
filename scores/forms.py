from django.forms import ModelForm
from django.contrib.admin import widgets
from django import forms
from handicap.scores.models import Score

class ScoreForm(ModelForm):
    date = forms.DateField(widget=widgets.AdminDateWidget)

    class Meta:
        model = Score
        exclude = ('golfer',)
