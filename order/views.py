from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse


from .forms import OrderCreateForm, PhoneForm
from movie.session import SessionTickets
from movie.models import Ticket
# Create your views here.


class CreateOrderView(View):

    def post(self, request, slug):
        tickets = SessionTickets(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in tickets.get():
                ticket = Ticket.objects.get(id=item)
                ticket.order = order
                ticket.save()
            order.price = order.get_total_cost()
            order.save()
            tickets.clear()
            request.session['order_id'] = order.id
            return redirect('process', slug=slug)
        request.session['error_email'] = form.errors
        # messages.add_message(request, messages.ERROR, "Форма не валидный")
        return redirect('order_create', slug=slug)

    def get(self, request, slug):
        tickets_ids = SessionTickets(request)
        try:
            tickets = [Ticket.objects.get(id=id) for id in tickets_ids.get()]
        except Ticket.DoesNotExist:
            return redirect('today', slug=slug)
        if tickets:
            total_price = tickets[0].session.price * len(tickets)
        else: 
            return redirect('today', slug=slug)
        
        errors = request.session.get('error_email', '')
        if request.session.get('error_email', ''):
            del request.session['error_email']
        
        errors2 = request.session.get('error_password', '')
        if request.session.get('error_password', ''):
            del request.session['error_password']

        errors3 = request.session.get('error_all', '')
        if request.session.get('error_all', ''):
            del request.session['error_all']

        print('=============', errors2)
            
        form_two = PhoneForm()
        form = OrderCreateForm()
        return render(request, 'orders/create.html', {'form_one': form,
                                                      'form_two': form_two, 
                                                      'slug': slug,
                                                      'tickets_count': len(tickets),
                                                      'total_price': total_price,
                                                      'errors': errors,
                                                      'errors2': errors2,
                                                      'errors3': errors3})


class CancelTickets(View):

    def get(self, request, slug):
        tickets = SessionTickets(request)
        session = None
        for item in tickets.get():
            ticket = Ticket.objects.get(id=item)
            session = ticket.session.id
            ticket.delete()
        if not session:
            return redirect('today', slug=slug)
        return redirect('session_detail', slug=slug, pk=session)