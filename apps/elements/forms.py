from django import forms
from .models import Respondent, Question, Answer

class RespondentForm(forms.ModelForm):
    class Meta:
        model = Respondent
        fields = '__all__'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('respondent', 'question', 'choice')
