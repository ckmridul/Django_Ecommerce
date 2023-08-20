from django.db import models
from base.models import BaseModel
from account.models import Profile
from product.models import Product,ProductVariant


# Create your models here.

class Address(BaseModel):
    user =  models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='address', blank=True, null=True)
    session_id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    landmark = models.CharField(max_length=100, blank= True, null=True)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    state = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.IntegerField()
    alternate_number =models.IntegerField(blank=True,null=True)
    
    
class Wishlist(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wishlist', blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    

class Wishlistitem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlistitem')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    
    


