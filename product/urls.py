from django.urls import path
from . import views


urlpatterns = [
    path("<slug>/", views.get_product, name="get_product"),
    path("add_to_cart/<uuid:uid>/", views.add_to_cart, name="add_to_cart"),
]
