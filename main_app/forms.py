from django.forms import ModelForm
from .models import Session

class SessionForm(ModelForm):
  class Meta:
    model = Session
    fields = ['date', 'occasion']
