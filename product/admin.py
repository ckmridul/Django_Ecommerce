from django.contrib import admin
from .models import *


class ProductImageAdmin(admin.StackedInline):
    model = Productimage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Productimage)
admin.site.register(ProductVariant)
admin.site.register(Coupon)
admin.site.register(Offer)
