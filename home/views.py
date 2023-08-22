from django.shortcuts import render
from product.models import Product, Offer, Category, ProductVariant
from django.http import JsonResponse
from account.models import Cart, CartItem
from base.session_key import session_key


# Create your views here.
def index(request):
    context = {
        "products": Product.objects.filter(status=True),
        "offers": Offer.objects.all(),
        "catagories": Category.objects.all(),
    }

    return render(request, "home/home.html", context)


def get_similar_products(request):
    if request.method == "GET":
        search_term = request.GET.get("search_term", "")
        similar_products = Product.objects.filter(product_name__icontains=search_term)[
            :10
        ]
        data = {
            "products": [
                {"id": product.uid, "name": product.product_name}
                for product in similar_products
            ]
        }
        return JsonResponse(data)
    return JsonResponse({}, status=400)


def searched(request):
    p_id = request.GET.get("searched")
    product = Product.objects.get(uid=p_id)
    context = {
        "product": product,
        "selected_ram": product.productVariant.first().ram,
        "selected_variant": product.productVariant.first(),
    }
    return render(request, "product/product.html", context)


def search_result(request):
    search = request.GET["searched"]
    products = Product.objects.filter(product_name__icontains=search)
    context = {"products": products, "search": search}
    return render(request, "home/search_result.html", context)


def shop(request):
    product = Product.objects.filter(status=True)
    if request.method == "POST":
        price = request.POST["price"]
        if price == "-20,000":
            variant = ProductVariant.objects.filter(price__lt=20000)
            products = [item["product"] for item in variant.values("product")]
            product = Product.objects.filter(uid__in=products, status=True).distinct()
        elif price == "-50,000":
            variant = ProductVariant.objects.filter(price__lt=50000)
            products = [item["product"] for item in variant.values("product")]
            product = Product.objects.filter(uid__in=products, status=True).distinct()
        elif price == "50,000+":
            variant = ProductVariant.objects.filter(price__gt=50000)
            products = [item["product"] for item in variant.values("product")]
            product = Product.objects.filter(uid__in=products, status=True).distinct()
        else:
            product = Product.objects.filter(status=True)

    context = {
        "products": product,
        "catagory_name": "Shop",
        "catagories": Category.objects.all(),
    }
    return render(request, "home/shop_catagory.html", context)


def catagory_show(request, uid):
    all_catagory = Category.objects.all()
    catagory = Category.objects.get(uid=uid)
    product = Product.objects.filter(category=catagory)

    context = {
        "products": product,
        "catagory_name": catagory.category_name,
        "catagories": Category.objects.all(),
    }
    return render(request, "home/shop_catagory.html", context)


def cart_counter(request):
    print("cart_counter")
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_count = cart_items.count()
        data = {"cart_count": cart_count}
        return JsonResponse(data)
    else:
        cart_items = CartItem.objects.filter(cart__session_id=session_key(request))
        cart_count = cart_items.count()
        data = {"cart_count": cart_count}
        return JsonResponse(data)
