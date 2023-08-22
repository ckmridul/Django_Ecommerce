from django.urls import path
from . import views

urlpatterns = [
    path("my_profile/", views.user_profile, name="userprofile"),
    path("change_password/", views.change_password, name="change_password"),
    path("add_address/", views.add_address, name="add_address"),
    path("update_address/<uuid:uid>/", views.update_address, name="update_address"),
    path("cart/", views.cart_view, name="cart"),
    path("update_cart/", views.update_cart, name="update_cart"),
    path(
        "delete_cart_item/<uuid:uid>/", views.delete_cart_item, name="delete_cart_item"
    ),
    path("remove_coupon/", views.remove_coupon, name="remove_coupon"),
    path("order/", views.make_order, name="make_order"),
    path("myOrder/", views.myOrder, name="myOrder"),
    path("view_user_order/<uuid:uid>/", views.view_user_order, name="view_user_order"),
    path("cancel_order/<uuid:uid>/", views.cancel_order, name="cancel_order"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path(
        "add_wishlist/<uuid:v_uid>/<uuid:p_uid>/",
        views.add_wishlist,
        name="add_wishlist",
    ),
    path("delete_wishlist/<uuid:uid>", views.delete_wishlist, name="delete_wishlist"),
    path(
        "add_to_cart_from_wish/<uuid:uid>/",
        views.add_to_cart_from_wish,
        name="add_to_cart_from_wish",
    ),
]
