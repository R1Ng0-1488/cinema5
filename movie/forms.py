from django import forms
from django.db.utils import IntegrityError

from .models import Ticket, Place


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('place', 'session')

    def __init__(self, *args, **kwargs):
        self.places = args[0].getlist('place')
        super().__init__(*args, **kwargs)

    def save(self):
        tickets = []
        for place in self.places:
            tickets.append(Ticket.objects.create(place=Place.objects.get(id=place),
                                                 session=self.cleaned_data['session']))
        return [ticket.id for ticket in tickets]
