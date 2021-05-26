from cinema5.celery import app

from .models import Ticket


@app.task
def delete_tickets_if_invalid(tickets):

    t = [Ticket.objects.get(id=pk) for pk in tickets]
    if t[0].order:
        if not t[0].order.paid:
            t[0].order.delete()
    else:
        for ticket in t:
            ticket.delete()
