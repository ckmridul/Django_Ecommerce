from django.urls import path
from . import views


urlpatterns = [
    path("place_order/", views.place_order, name="place_order"),
    path("payment/", views.payment, name="payment"),
    path("order_complete", views.order_complete, name="order_complete"),
    path(
        "download_invoice/<uuid:uid>/", views.download_invoice, name="download_invoice"
    ),
]
