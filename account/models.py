from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel
from product.models import Product, ProductVariant, Coupon

# Create your models here.

class Profile(AbstractUser):
    phone = models.IntegerField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to= 'profile')
    
    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid = False, cart__user = self).count()
    
    
class Cart(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='carts', blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total_price(self):
        return self.variant.price * self.quantity
    