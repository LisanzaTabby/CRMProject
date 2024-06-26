from django.forms import inlineformset_factory
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .models import *
from .forms import *
from .filter import OrderFilter
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@login_required(login_url='loginPage')
@admin_only
def home(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers, 'products': products, 'orders': orders, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}

    return render(request, 'accounts/dashboard.html',context)
def UserPage(request):
	context = {}
	return render(request, 'accounts/user.html', context)
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def products(request):
	
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user= form.save()
			username = form.cleaned_data.get('username')
#associating a registering user with a system role of customer
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			messages.success(request, 'Account successfully created for '+username, '!')
			return redirect('loginPage')
	context= {'form':form}
	return render(request, 'accounts/register.html',context)
@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
			
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'USERNAME or PASSWORD is INCORRECT!')
	context = {}
	return render(request, 'accounts/login.html', context)
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	
	orders = customer.order_set.all()
	order_count = orders.count()
	myFilter = OrderFilter(request.POST, queryset=orders)
	# below code is rebuilding our orders variable to the myFilter model.queryset
	orders = myFilter.qs


	context = {'customer':customer,'myFilter': myFilter,'orders': orders, 'order_count': order_count}

	return render(request, 'accounts/customer.html', context)
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset':formset}
	return render(request, 'accounts/order_form.html', context)
'''def createCustomer(request):
      form = CustomerForm()
      if request.method == 'POST':
            form = CustomerForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect('/')
            context =  {'form':form}
            return render(request, 'accounts/customer_form.html', context)'''
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	
	return render(request, 'accounts/order_form.html', context)
@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	
	return render(request, 'accounts/delete.html', context)
def logoutView(request):
	logout(request)
	return redirect('loginPage')
