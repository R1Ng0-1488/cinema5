from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import auth

import braintree
from order.models import Order
# Create your views here.


class PaymentProcess(View):

    def post(self, request, slug):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        # get the token dor creating a transaction
        nonce = request.POST.get('payment_method_nonce', None)
        # Create and save the transaction
        result = braintree.Transaction.sale({
            'amount': f'{order.price}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        print('22222')
        if result.is_success:
            if order.discount:
                request.user.bonuses -= order.discount
                request.user.save()

            if order.user and order.discount == 0:
                request.user.bonuses += order.price / 100 * 5
                request.user.save()
            print('22222')
            # order mark like paid
            order.paid = True
            # save transaction id in order
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('done', slug=slug, pk=order_id)
        elif order.price == 0:
            print('22222')
            print('22222')
            if order.discount:
                request.user.bonuses -= order.discount
                request.user.save()
                order.paid = True
                order.save()
                return redirect('done', slug=slug, pk=order_id)
        else:
            return redirect('canceled', slug=slug)

    def get(self, request, slug):
        # form token for JS SDK
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order,
                                                        'client_token': client_token,
                                                        'slug': slug})


class PaymentDone(View):
    def get(self, request, slug, pk):
        if request.user:
            if not request.user.is_staff:
                auth.logout(request)
        order = get_object_or_404(Order, id=pk)
        tickets = order.ticket_set.all()
        row_set = {ticket.place.row.row for ticket in tickets}
        return render(request, 'payment/done.html', {'order': order, 'tickets': tickets, 'row_set': row_set})


class PaymentCanceled(View):
    def get(self, request, slug):
        # if request.user:
        #     auth.logout(request)
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        session = order.ticket_set.first().session.id
        print('aaaaaaaaaaaaaaa', session, order_id)
        order.delete()
        return redirect('session_detail', slug=slug, pk=session)
