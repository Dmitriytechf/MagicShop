from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from cart.cart import Cart

from .forms import ShipingAdressForm
from .models import ShipingAdress, Order, OrderItem


@login_required(login_url='account:login')
def shiping(request):
    """
    Обработчик формы доставки. Позволяет пользователю:
    1. Просматривать существующие данные доставки
    2. Создавать новую запись доставки
    3. Обновлять существующую запись
    """
    try:
        shiping_adress = ShipingAdress.objects.get(user=request.user)
    except ShipingAdress.DoesNotExist:
        shiping_adress = None
    
    # instance=shiping_adress - если адрес существует, форма заполнится его данными
    form = ShipingAdressForm(instance=shiping_adress)
    
    if request.method == 'POST':
        # Создаем форму с переданными данными и привязкой к существующему адресу
        form = ShipingAdressForm(request.POST, instance=shiping_adress)

        if form.is_valid():
            shiping_adress = form.save(commit=False)
            # Привязываем адрес к текущему пользователю
            shiping_adress.user = request.user
            form.save()
            return redirect('account:profile')
        
    return render(request, 'payment/shiping.html', {'form': form})


def checkout(request):
    """
    Возвращаем шаблон с переданными данными достваки
    """
    if request.user.is_authenticated:
        shiping_adress = get_object_or_404(ShipingAdress, user=request.user)
        if shiping_adress:
            return render(request, 'payment/checkout.html', {'shiping_adress': shiping_adress})

    return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        street_adress = request.POST.get('street_adress')
        apartment_adress = request.POST.get('apartment_adress')
        country = request.POST.get('country')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        
        # Создаем экземпляр корзины и берем всю сумму
        cart = Cart(request) 
        totap_price = cart.get_total_price()
        
        shiping_adress, _ = ShipingAdress.objects.get_or_create(
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
        
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, 
                                         shiping_adress=shiping_adress,
                                         anount=totap_price)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['qty'], user=request.user)
        else:
            order = Order.objects.create(shiping_adress=shiping_adress,
                                         anount=totap_price)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['qty'])

        return JsonResponse({'success': True})


def payment_success(request):
    pass


def payment_fail(request):
    return render(request, 'payment/payment-fail.html')