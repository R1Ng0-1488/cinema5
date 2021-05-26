from django.shortcuts import render, redirect
from django.views.generic import View, edit
from django.contrib.auth import authenticate, login, views

from .models import AdvUser
from order.models import Order
from movie.models import Ticket
from order.forms import CustomUserCreationForm, OrderCreateForm
from movie.session import SessionTickets
from django.core.cache import cache
from django.conf import settings

import redis

from .forms import LoginForm, AdvUserUpdateForm, RegisterForm
from order.forms import PhoneForm


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


class CheckEmail(View):
	def post(self, request):
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		form = PhoneForm(request.POST)
		# if form.is_valid():
		try: 
			AdvUser.objects.get(email=email)
			l = LoginForm(data={'username': email, 'password': password})
			if l.is_valid():
				user = authenticate(email=email, password=password)
				login(request, user)
				return redirect('account')
			request.session['error_password'] = l.errors
			request.session['error_all'] = l.non_field_errors()
			return redirect('check_email')		


		except AdvUser.DoesNotExist: 
			print('asss')
			reg = RegisterForm(data={'username': email, 'password1': password, 'password2': password})
			if reg.is_valid():
				AdvUser.objects.create_user(email=email, password=password)
				user = authenticate(email=email, password=password)
				login(request, user)
				return redirect('account')
			request.session['error_password'] = reg.errors
			request.session['error_all'] = reg.non_field_errors()
			return redirect('check_email')	

		# print(request.POST)

		# form = PhoneForm(data=request.POST)
		# if form.is_valid():
		# 	email = request.POST.get('email', '')
		# 	password = request.POST.get('password', '')
		# 	user = authenticate(email=email, password=password)
		# 	if user:
		# 		login_form = LoginForm(request.POST)
		# 		if login_form.is_valid():
		# 			login(request, user)
		# 			return redirect('account')
		# 		else:
		# 			request.session['error_password'] = form.errors
		# 			return redirect('order_create', slug=r.get('const_city').decode())
		# 	else: 
		# 		register_form = RegisterForm(data={'username': email,
		# 										   'password1': password,
		# 										   'password2': password})
		# 		if register_form.is_valid():
		# 			AdvUser.objects.create_user(email=email, password=password)
		# 			user = authenticate(email=email, password=password)
		# 			login(request, user)
		# 			return redirect('account')
		# 		else:
		# 			request.session['error_password'] = form.errors
		# 			return redirect('order_create', slug=r.get('const_city').decode())
		# request.session['error_password'] = form.errors
		# return redirect('order_create', slug=r.get('const_city').decode())


	def get(self, request):
		form = PhoneForm()
		errors2 = request.session.get('error_password', '')
		if request.session.get('error_password', ''):
			del request.session['error_password']

		errors3 = request.session.get('error_all', '')
		if request.session.get('error_all', ''):
			del request.session['error_all']

		return render(request, 'user/check_email.html', {'form': form,
														 'errors2': errors2,
                                                      	 'errors3': errors3})


class Account(View):
	def get(self, request):
		return render(request, 'user/account.html')


class CheckPhone(View):
	def post(self, request):
		email = request.POST.get('email', '')
		password = request.POST.get('password', '')
		form = PhoneForm(request.POST)
		# if form.is_valid():
		try: 
			AdvUser.objects.get(email=email)
			l = LoginForm(data={'username': email, 'password': password})
			if l.is_valid():
				user = authenticate(email=email, password=password)
				login(request, user)
				return redirect('use_bonuses')
			request.session['error_password'] = l.errors
			request.session['error_all'] = l.non_field_errors()
			return redirect('order_create', slug=r.get('const_city').decode())		


		except AdvUser.DoesNotExist: 
			print('asss')
			reg = RegisterForm(data={'username': email, 'password1': password, 'password2': password})
			if reg.is_valid():
				AdvUser.objects.create_user(email=email, password=password)
				user = authenticate(email=email, password=password)
				login(request, user)
				return redirect('use_bonuses')
			request.session['error_password'] = reg.errors
			request.session['error_all'] = reg.non_field_errors()
			return redirect('order_create', slug=r.get('const_city').decode())	
	
		# request.session['error_password'] = form.errors
		# return redirect('order_create', slug=r.get('const_city').decode())		

class CreateUserOrderView(View):

	def get(self, request):
		user = request.user
		bonuses = user.bonuses

		print('---------->', user)

		tickets = SessionTickets(request)
		total_price = tickets.total_price()
		one_price = tickets.one_price()

		return render(request, 'user/use_bonuses.html', {'bonuses': bonuses,
														 'total_price': total_price,
														 'one_price': one_price,
														 'ticket_count': tickets.len()})

	def post(self, request):
		bonus = request.POST.get('bonus', '')
		# request.session['bonus'] = bonus
		# return redirect('process', slug=slug)
		print(type(bonus), bonus)
		slug = r.get('const_city').decode()
		tickets = SessionTickets(request)
		user = request.user 
		if bonus:
			if user.bonuses >= tickets.total_price():
				# и вычитать бонусы только после оплаты
				bonuses = tickets.total_price()
				price = 0
			elif user.bonuses < tickets.total_price():
				price = tickets.total_price() - user.bonuses
				bonuses = user.bonuses

			order = Order.objects.create(email=user.email, user=user, price=price, discount=bonuses)
			for item in tickets.get():
				ticket = Ticket.objects.get(id=item)
				ticket.order = order
				ticket.save()
			tickets.clear()
			request.session['order_id'] = order.id
			return redirect('process', slug=slug)
		else:
			price = tickets.total_price()
			# потом переделать чтобы бонусы добавлялись только после оплаты
			order = Order.objects.create(email=user.email, user=user, price=price)
			for item in tickets.get():
				ticket = Ticket.objects.get(id=item)
				ticket.order = order
				ticket.save()
			tickets.clear()
			request.session['order_id'] = order.id
			return redirect('process', slug=slug)
			

    # def post(self, request, slug):
    #     tickets = SessionTickets(request)
    #     form = OrderCreateForm(request.POST)
    #     if form.is_valid():
    #         order = form.save()
    #         for item in tickets.get():
    #             ticket = Ticket.objects.get(id=item)
    #             ticket.order = order
    #             ticket.save()
    #         tickets.clear()
    #         request.session['order_id'] = order.id
    #         return redirect('process', slug=slug)
    #     messages.add_message(request, messages.ERROR, "Форма не валидный")
    #     return redirect('order_create', slug=slug)


def lol(request, slug):
	print(request.user)
	return render(request, '1.html')


class UpdateAccountView(edit.UpdateView):
	model = AdvUser
	form_class = AdvUserUpdateForm
	success_url = '/account/acoount/'
	template_name = 'user/update_account.html'