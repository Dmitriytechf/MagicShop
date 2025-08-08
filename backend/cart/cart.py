from decimal import Decimal

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from shop.models import ProductProxy


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        
        if not cart:
            cart =  self.session['session_key'] = {}
            
        self.cart = cart

 
    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())


    def __iter__(self):
        product_ids = self.cart.keys() 
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def add(self, product, quantity):
        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['qty'] += quantity
        else:
            self.cart[product_id] = {'qty': quantity, 'price': str(product.price)}
        
        self.session.modified = True
    
    
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
            self.session.modified = True


    def update(self, product, quantity):
        product_id = str(product)
        
        if product_id in self.cart:
            self.cart[product_id]['qty'] = quantity
            self.session.modified = True


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    
    
    def save_to_user(self):
        """Сохраняет корзину в профиль пользователя"""
        # Проверяем аутентификацию через request
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            user = self.request.user
            # Проверяем наличие профиля
            if hasattr(user, 'profile'):
                user.profile.cart_data = self.cart
                user.profile.save()


    def restore_from_user(self):
        """Восстанавливает корзину из профиля пользователя"""
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            user = self.request.user
            if hasattr(user, 'profile') and user.profile.cart_data:
                self.cart = user.profile.cart_data
                self.session['session_key'] = self.cart
                self.session.modified = True


@receiver(user_logged_out)
def save_cart_on_logout(sender, request, user, **kwargs):
    """Сохраняет корзину при выходе"""
    cart = Cart(request)
    cart.save_to_user()  # сохраняем корзину в профиль

@receiver(user_logged_in)
def restore_cart_on_login(sender, request, user, **kwargs):
    """Восстанавливает корзину при входе"""
    cart = Cart(request)
    cart.restore_from_user() # восстанавливаем корзину из профиля
