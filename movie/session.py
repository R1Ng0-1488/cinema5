from cinema5.settings import CHOSEN_TICKETS

from .models import Ticket


class SessionTickets:
    def __init__(self, request):
        self.session = request.session
        tickets = self.session.get(CHOSEN_TICKETS)
        if not tickets:
            tickets = self.session[CHOSEN_TICKETS] = []
        self.tickets = tickets

    def add(self, tickets):
        self.session[CHOSEN_TICKETS] = tickets

    def clear(self):
        self.session[CHOSEN_TICKETS] = []

    def get(self):
        return self.tickets

    def len(self):
        return len(self.tickets)

    def one_price(self):
        if len(self.tickets) > 0:
            ticket = Ticket.objects.get(id=self.tickets[0])
            return ticket.session.price
            
    def total_price(self):
        if len(self.tickets) > 0:
            ticket = Ticket.objects.get(id=self.tickets[0])
            return ticket.session.price * len(self.tickets)
        return 0

    def __iter__(self):
        yield from self.tickets
