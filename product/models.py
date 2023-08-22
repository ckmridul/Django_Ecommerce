from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.


class Offer(BaseModel):
    name = models.CharField(max_length=50)
    percentage = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="catgories")
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="brand_imgs/")

    def __str__(self):
        return self.title


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    product_description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )
    status = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

    def get_variants_by_ram(self, ram):
        return self.productVariant.get(ram=ram)

    def get_offer_price(self, variant):
        variant = variant
        p_price = 0
        c_price = 0
        if self.offer:
            p_price = variant.price - (variant.price * (self.offer.percentage / 100))

        if self.category.offer:
            c_price = variant.price - (
                variant.price * (self.category.offer.percentage / 100)
            )

        if p_price and c_price:
            price = min(p_price, c_price)
        elif p_price and not c_price:
            price = p_price
        elif not p_price and c_price:
            price = c_price
        else:
            price = 0

        return price


class Productimage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(upload_to="product")

    class Meta:
        ordering = ["-image"]


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="productVariant"
    )
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    color = models.CharField(max_length=10)
    ram = models.CharField(max_length=10)
    storage = models.CharField(max_length=10)

    def __str__(self):
        return str(self.price)


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
