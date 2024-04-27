# forms.py

from django import forms
from .models import Event,EventRegistration

class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['event','Name', 'Register_No', 'year', 'Department', 'Specialization','Section','Email','Phone_No','Event_Name']
        widgets = {
            'event': forms.HiddenInput(),
            'Event_Name': forms.HiddenInput(),  # Use HiddenInput widget for the event field
        }

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)
        super().__init__(*args, **kwargs)
        if event_id:
            self.fields['event'].initial = event_id
            self.fields['event'].widget.attrs['readonly'] = True
            event_name = Event.objects.get(pk=event_id).Event_Name
            self.fields['Event_Name'].initial = event_name

class UserSelectForm(forms.Form):
    var1 = forms.ModelChoiceField(queryset=EventRegistration.objects.all(), label="Select User")
