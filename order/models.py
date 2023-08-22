from django.db import models
from base.models import BaseModel
from account.models import Profile
from user.models import Address
from product.models import Product,ProductVariant

# Create your models here. 

class Payment(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=10)
    status = models.CharField(max_length=50)
    
    def __str__(self):
        return self.payment_id
    
class Order(BaseModel):
    status_choice = (
        ('Order placed','Order placed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
    )
    
    user = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name="orders", blank=True, null=True)
    session_id = models.CharField(max_length=100)
    payment = models.ForeignKey(Payment, on_delete = models.SET_NULL, blank=True,null=True)
    order_number = models.CharField(max_length=20)
    coupon_price = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    order_total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=status_choice, default='Order Pending')
    is_orderd = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created_at']
    

class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderproduct')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.product.product_name
    
    