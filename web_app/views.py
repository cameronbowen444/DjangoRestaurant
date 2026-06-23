from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User, Customer, Category, Item, UserItem
import bcrypt


def setup_cart(request):
    if 'cart_item' not in request.session:
        request.session['cart_item'] = 0

    if 'order' not in request.session:
        request.session['order'] = []


def index(request):
    setup_cart(request)

    context = {
        'food': Item.objects.filter(category=1),
        'cart_item': request.session['cart_item'],
        'order': request.session['order']
    }

    return render(request, 'index.html', context)


def menu(request):
    setup_cart(request)

    context = {
        'apps': Item.objects.filter(category=1),
        'pizza': Item.objects.filter(category=2),
        'pasta': Item.objects.filter(category=3),
        'desserts': Item.objects.filter(category=4),
        'drinks': Item.objects.filter(category=5),
        'cart_item': request.session['cart_item'],
        'order': request.session['order'],
    }

    return render(request, 'menu.html', context)


def clean_order(order):
    cleaned_order = []

    for item in order:
        if isinstance(item, dict):
            if 'quantity' not in item:
                item['quantity'] = 1

            cleaned_order.append(item)

    return cleaned_order


def calculate_cart(order, apply_discount=False):
    subtotal = 0

    for item in order:
        item['item_total'] = round(float(item['price']) * int(item['quantity']), 2)
        subtotal += item['item_total']

    subtotal = round(subtotal, 2)

    discount = 0
    if apply_discount:
        discount = round(subtotal * 0.15, 2)

    discounted_subtotal = round(subtotal - discount, 2)
    tax = round(discounted_subtotal * 0.095, 2)
    total = round(discounted_subtotal + tax, 2)

    return subtotal, discount, tax, total


def cart(request):
    setup_cart(request)

    order = request.session['order']
    cleaned_order = clean_order(order)

    apply_discount = 'user_id' in request.session
    subtotal, discount, tax, total = calculate_cart(cleaned_order, apply_discount)

    request.session['order'] = cleaned_order
    request.session['cart_item'] = sum(item['quantity'] for item in cleaned_order)
    request.session.modified = True

    context = {
        'order': cleaned_order,
        'cart_item': request.session['cart_item'],
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'apply_discount': apply_discount,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request, item_id):
    setup_cart(request)

    item = Item.objects.get(id=item_id)
    order = request.session['order']

    item_exists = False

    for cart_item in order:
        if isinstance(cart_item, dict) and cart_item['id'] == item.id:
            cart_item['quantity'] += 1
            item_exists = True
            break

    if not item_exists:
        order.append({
            'id': item.id,
            'name': item.food_name,
            'price': float(item.price),
            'quantity': 1,
        })

    request.session['order'] = order
    request.session['cart_item'] = sum(
        item['quantity'] for item in order if isinstance(item, dict)
    )
    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'cart_item': request.session['cart_item'],
            'message': 'Item added to cart'
        })

    return redirect('/menu')


def increase_quantity(request, item_id):
    setup_cart(request)

    order = clean_order(request.session['order'])

    for item in order:
        if item['id'] == item_id:
            item['quantity'] += 1
            break

    request.session['order'] = order
    request.session['cart_item'] = sum(item['quantity'] for item in order)
    request.session.modified = True

    return redirect('/cart')


def decrease_quantity(request, item_id):
    setup_cart(request)

    order = clean_order(request.session['order'])

    for item in order:
        if item['id'] == item_id:
            item['quantity'] -= 1

            if item['quantity'] <= 0:
                order.remove(item)

            break

    request.session['order'] = order
    request.session['cart_item'] = sum(item['quantity'] for item in order)
    request.session.modified = True

    return redirect('/cart')


def remove_from_cart(request, item_id):
    setup_cart(request)

    order = clean_order(request.session['order'])
    order = [item for item in order if item['id'] != item_id]

    request.session['order'] = order
    request.session['cart_item'] = sum(item['quantity'] for item in order)
    request.session.modified = True

    return redirect('/cart')


def checkout(request):
    setup_cart(request)

    order = request.session['order']
    cleaned_order = clean_order(order)

    apply_discount = 'user_id' in request.session
    subtotal, discount, tax, total = calculate_cart(cleaned_order, apply_discount)

    request.session['order'] = cleaned_order
    request.session['cart_item'] = sum(item['quantity'] for item in cleaned_order)
    request.session.modified = True

    context = {
        'order': cleaned_order,
        'cart_item': request.session['cart_item'],
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'apply_discount': apply_discount,
    }

    return render(request, 'checkout.html', context)


def post_checkout(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']

    Customer.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )

    request.session['cart_item'] = 0
    request.session['order'] = []
    request.session.modified = True

    return redirect('/?order=placed')


def login(request):
    setup_cart(request)

    return render(request, 'login.html')


def post_login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/login')

    user = User.objects.filter(email=request.POST['email'])
    request.session['user_id'] = user[0].id

    return redirect('/')


def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/login')

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=pw_hash
    )

    request.session['user_id'] = user.id

    return redirect('/')


def logout(request):
    request.session.clear()

    return redirect('/')