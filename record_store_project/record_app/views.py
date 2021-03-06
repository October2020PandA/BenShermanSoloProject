from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import random
import bcrypt

def index(request):
    if 'order_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        current_order = Order.objects.get(id=request.session['order_id'])
        item_tally = current_order.orderitem_set.count()
        context = {
            'item_tally': item_tally,
        }
        return render (request, 'index.html', context)
    else:
        context = {
            'item_tally': 0,
        }
        return render (request, 'index.html', context)
def equipment(request):
    return render (request, 'equipment.html')

def records(request):
    if 'order_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        current_order = Order.objects.get(id=request.session['order_id'])
        item_tally = current_order.orderitem_set.count()
        context = {
            'item_tally': item_tally,
            'product_list' : Product.objects.order_by('artist'),
        }
        return render (request, 'records.html', context)
    else:
        context = {
            'item_tally': 0,
            'product_list' : Product.objects.order_by('artist'),
        }
        return render (request, 'records.html', context)

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
        return redirect('/')
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
        return redirect('/')
    return redirect('/register_page')

def add_product(request):
    return render (request, 'add_product.html')

def products(request):
    context = {
        'products': Product.objects.all(),
    }
    return render (request, 'products_table.html', context)

def item(request, product_id):
    if 'order_id' in request.session:
        this_product = Product.objects.get(id=product_id)
        same_genre_list = Product.objects.filter(genre=this_product.genre).exclude(id=this_product.id)
        this_user = User.objects.get(id=request.session['user_id'])
        current_order = Order.objects.get(id=request.session['order_id'])
        item_tally = current_order.orderitem_set.count()
        context = {
            'item_tally': item_tally,
            'product': Product.objects.get(id=product_id),
            'similar_items': Product.objects.filter(genre=this_product.genre).exclude(id=this_product.id)
        }
        return render (request, 'item.html', context)
    else:
        this_product = Product.objects.get(id=product_id)
        same_genre_list = Product.objects.filter(genre=this_product.genre).exclude(id=this_product.id)
        context = {
            'item_tally': 0,
            'product': Product.objects.get(id=product_id),
            'similar_items': Product.objects.filter(genre=this_product.genre).exclude(id=this_product.id)
        }
        return render (request, 'item.html', context)
        

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/login')
    if 'order_id' in request.session:
        if request.method == "POST":
            current_user = User.objects.get(id=request.session['user_id'])
            current_product = Product.objects.get(id=product_id)
            current_order = Order.objects.get(id=request.session['order_id'])
            OrderItem.objects.create(
                product = current_product,
                order = current_order,
                quantity = request.POST['quantity']
            )
            return redirect(f'/item/{product_id}')
    else:
        if request.method == "POST":
            current_user = User.objects.get(id=request.session['user_id'])
            current_product = Product.objects.get(id=product_id)
            current_order = Order.objects.create(
                ordered_by = current_user,
                ship_to = None,
                charged_to = None,
                is_complete= False,
            )
            OrderItem.objects.create(
                product = current_product,
                order = current_order,
                quantity = request.POST['quantity']
            )
            request.session['order_id'] = current_order.id 
            return redirect(f'/item/{product_id}')

def checkout(request):
    if 'user_id' not in request.session:
        return redirect ('/login_page')
    if 'order_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        current_order = Order.objects.get(id=request.session['order_id'])
        item_tally = current_order.orderitem_set.count()
        items = current_order.orderitem_set.all() 
        context = {
            'item_tally' : item_tally,
            'items': items,
            'order': current_order,
        }
        if request.method == "POST":
            errors = ShippingAddress.objects.shipping_address_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect ('/checkout')
            errors = BillingAddress.objects.billing_address_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect ('/checkout')
            return redirect ('/confirmation')
        return render (request, 'checkout.html', context)
    else:
        this_user = User.objects.get(id=request.session['user_id'])
        context = {
            'item_tally' : 0,
        }
        return render (request, 'checkout.html', context)

def confirmation(request):
    if 'user_id' not in request.session:
        return redirect ('/login_page')

    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render (request, 'confirmation.html', context)

def delete(request, orderitem_id):
    this_orderitem = OrderItem.objects.get(id=orderitem_id)
    this_orderitem.delete()
    return redirect('/checkout')

    
def orders(request):
    return render (request, 'orders_table.html')

def logout(request):
    request.session.clear()
    return redirect('/logout_page')

def logout_page(request):
    return render(request, 'logout_page.html')