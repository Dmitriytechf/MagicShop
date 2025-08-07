from decimal import Decimal

import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from django.conf import settings
from cart.cart import Cart

from .forms import ShipingAdressForm
from .models import ShipingAdress, Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required(login_url='account:login')
def shiping(request):
    '''
    Обработчик формы доставки. Позволяет пользователю:
    1. Просматривать существующие данные доставки
    2. Создавать новую запись доставки
    3. Обновлять существующую запись
    '''
    try:
        shipping_adress = ShipingAdress.objects.get(user=request.user)
    except ShipingAdress.DoesNotExist:
        shipping_adress = None
    
    # instance=shipping_adress - если адрес существует, форма заполнится его данными
    form = ShipingAdressForm(instance=shipping_adress)
    
    if request.method == 'POST':
        # Создаем форму с переданными данными и привязкой к существующему адресу
        form = ShipingAdressForm(request.POST, instance=shipping_adress)

        if form.is_valid():
            shipping_adress = form.save(commit=False)
            # Привязываем адрес к текущему пользователю
            shipping_adress.user = request.user
            form.save()
            return redirect('account:profile')
        
    return render(request, 'payment/shiping.html', {'form': form})


def checkout(request):
    '''
    Возвращаем шаблон с переданными данными достваки
    '''
    if request.user.is_authenticated:
        shipping_adress = get_object_or_404(ShipingAdress, user=request.user)
        if shipping_adress:
            return render(request, 'payment/checkout.html', {'shipping_adress': shipping_adress})

    return render(request, 'payment/checkout.html')


def complete_order(request):
    '''Обработка запроса при оформлении заказа'''
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        name = request.POST.get('name')
        email = request.POST.get('email')
        street_adress = request.POST.get('street_adress')
        apartment_adress = request.POST.get('apartment_adress')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')

        # Создаем экземпляр корзины и берем общую сумму
        cart = Cart(request) 
        total_price = cart.get_total_price()

        match payment_type:
            case "stripe-payment":
                shipping_adress, _ = ShipingAdress.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'full_name': name,
                        'email': email,
                        'street_adress': street_adress,
                        'apartment_adress': apartment_adress,
                        'country': country,
                        'city': city,
                        'zip_code': zipcode,
                    }
                )

                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse("payment:payment-success")),
                    'cancel_url': request.build_absolute_uri(reverse("payment:payment-fail")),
                    'line_items': []
                }

                if request.user.is_authenticated:
                    order = Order.objects.create(user=request.user, 
                                                shipping_adress=shipping_adress,
                                                amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'],
                                                price=item['price'], quantity=item['qty'], user=request.user)
                        session_data['line_items'].append({
                            'price_data':{
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product']
                                }
                            },
                            'quantity': item['qty'],
                        })

                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)
                else:
                    order = Order.objects.create(shipping_adress=shipping_adress,
                                                amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(order=order, product=item['product'],
                                                price=item['price'], quantity=item['qty'])
                        session_data['line_items'].append({
                            'price_data':{
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product']
                                }
                            },
                            'quantity': item['qty'],
                        })

                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)


def payment_success(request):
    '''
    Показываем подтверждение успешного заказа и очищаем текущуб сессию
    '''
    keys_to_delete = ['session_key', 'order_id']
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]
            request.session.modified = True # Явно сохраняем изменения сессии

    return render(request, 'payment/payment-success.html')


def payment_fail(request):
    '''Перенаправляем на страницу ошибки'''
    return render(request, 'payment/payment-fail.html')