from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.views.generic import (DetailView, ListView)
from django.utils.timezone import datetime


@unauthenticated_user
def registerPage(request):
    form = UserCreatedForm()
    if request.method == 'POST':
        form = UserCreatedForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user_name)
            return redirect('accounts:login')

    context = {'form': form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['customer'] = user.id
            request.session['email_id'] = user.email
            cart = {}
            request.session['cart'] = cart
            return redirect('accounts:homepage')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, "accounts/login.html")
    context = {}
    return render(request, "accounts/login.html", context)


def logoutPage(request):
    request.session.clear()
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs
    total_customers = customers.count()
    orders = Order.objects.all().order_by('-date_created')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'customers': customers, 'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered, 'pending': pending, 'myFilter': myFilter}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all().order_by('-date_created')
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    return render(request, 'accounts/customer.html', {'customer': customer, 'orders': orders,
                                                      'orders_count': orders_count, 'myFilter': myFilter})


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Product.objects.all().order_by('category')
    return render(request, 'accounts/products.html', {'products': product})


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'quantity', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    form = ProductForm()
    if (request.method == 'POST'):
        form = ProductForm(request.POST, request.FILES, )
        if form.is_valid():
            form.save()
            return redirect('accounts:products')
    context = {'form': form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if (request.method == 'POST'):
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('accounts:products')
    context = {'form': form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'customer'])
def updateOrder(request, pk):  #####################
    order = Order.objects.get(id=pk)
    form = UpdateForm(instance=order)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('accounts:homepage')
    context = {'order': order, 'form': form}
    return render(request, 'accounts/order_update.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def viewOrder(request, pk):  ###########3
    order = Order.objects.get(id=pk)
    context = {'order': order}
    return render(request, 'accounts/order_details.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('accounts:products')
    context = {'item': product}
    return render(request, 'accounts/delete_product.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userHomePage(request):
    prod = Product.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product1')
        quantity_add = request.POST.get('quantity1')
        if quantity_add:
            quantity_add = int(quantity_add)
            if quantity_add > 0:
                cart = request.session.get('cart')
                if cart:
                    quantity = cart.get(product)
                    if quantity:
                        cart[product] = quantity_add + quantity
                    else:
                        cart[product] = quantity_add
                else:
                    cart[product] = quantity_add
                request.session['cart'] = cart
                return redirect('/')
    cart = request.session.get('cart')
    print(cart)
    myFilter = ProductFilter(request.GET, queryset=prod)
    prod = myFilter.qs
    context = {'filter': myFilter, 'products': prod, 'cart': cart}
    return render(request, 'accounts/user_home.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userOrdersPage(request):
    orders = request.user.customer.order_set.all().order_by('status', 'date_created')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending,
               'myFilter': myFilter}
    return render(request, 'accounts/user_orders.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userAccountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/user_account_settings.html', context)


def placeOrder(request):
    cart = request.session.get('cart')
    for k, v in cart.items():
        customer = request.user.customer
        product = Product.objects.get(id=int(k))
        quantity = int(v)
        status = "Pending"
        Order.objects.create(customer=customer, product=product, quantity=quantity, status=status)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def userCartPage(request):
    cart = request.session.get('cart')
    if request.method == 'POST':
        placeOrder(request)
        cart = {}
        request.session['cart'] = cart
        return redirect('accounts:user_orders_page')
    context = {'cart': cart}
    return render(request, 'accounts/cart.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customer'])
def deletecartitem(request, pk):
    product = Product.objects.get(id=int(pk))
    cart = request.session.get('cart')
    quantity = cart.get(pk)
    if request.method == 'POST':
        cart.pop(pk)
        request.session['cart'] = cart
        return redirect('accounts:user_cart_page')
    context = {'quantity': quantity,'item': product}
    return render(request, 'accounts/remove_cart.html', context)
