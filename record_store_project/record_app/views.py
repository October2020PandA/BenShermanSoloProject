from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render (request, 'index.html')

def equipment(request):
    return render (request, 'equipment.html')

def records(request):
    context = {
        'product_list' : Product.objects.order_by('title'),
    }
    return render (request, 'records.html', context)

def item(request, product_id):
    context = {
        'product': Product.objects.get(id=product_id)
    }
    return render (request, 'item.html', context)

def login_page(request):
    return render(request, 'login_page.html')

def login(request):
    if request.method == "POST":
        errors = User.objects.log_in_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/login_page')
        this_user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = this_user.id
        return redirect('/checkout')
    return redirect('/login_page')

def register_page(request):
    return render (request, 'register_page.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/register_page')
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_password
        )
        request.session['user_id'] = new_user.id
        return redirect('/checkout')
    return redirect('/register_page')

def add_product(request):
    return render (request, 'add_product.html')

def products(request):
    context = {
        'products': Product.objects.all(),
    }
    return render (request, 'products_table.html', context)

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    elif request.method == "POST":
        this_order = Order.objects.create(
            quantity  = request.POST['quantity'],
        )
    return redirect(f'/checkout')

def checkout(request):
    if 'user_id' not in request.session:
        return redirect ('/login_page')
    if request.method == "POST":
        errors = ShippingAddress.objects.shipping_address_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/checkout')
    if request.method == "POST":
        errors = BillingAddress.objects.billing_address_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/checkout')
    if request.method == "POST":
        errors = Payment.objects.payment_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/checkout')
    else:
        context = {
            'current_order': Order.objects.all(),
        }
    return render (request, 'checkout.html', context)

def confirmation(request):
    if 'user_id' not in request.session:
        return redirect ('/login_page')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render (request, 'confirmation.html', context)

def orders(request):
    return render (request, 'orders_table.html')

def logout(request):
    request.session.clear()
    return redirect('/')
