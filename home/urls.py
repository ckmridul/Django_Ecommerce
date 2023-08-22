from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "get_similar_products/", views.get_similar_products, name="get_similar_products"
    ),
    path("searched/", views.searched, name="searched"),
    path("search_result/", views.search_result, name="search_result"),
    path("shop/", views.shop, name="shop"),
    path("catagory/<uuid:uid>/", views.catagory_show, name="catagory_show"),
    path("cart_counter/", views.cart_counter, name="cart_counter"),
]
