from django.contrib import admin
from .models import Address,Wishlist,Wishlistitem

# Register your models here.
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Wishlistitem)