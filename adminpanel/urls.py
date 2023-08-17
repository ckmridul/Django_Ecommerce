from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminpanel, name='adminpanel'),
    
    path('usermanage/',views.userMange, name='usermanage'),
    path('blockuser/<int:id>/',views.blockUser, name="blockuser"),
    
    path('catagory/', views.catagoryManage, name = 'catagory'),
    path('editcatagory/<uuid:uid>/', views.editcategory, name='editcategory'),
    path('delete_catagory/', views.delete_catagory, name='delete_catagory'),
    
    path('productviwe/', views.productview, name="product_view"),
    path('delete_product/<uuid:uid>/',views.delete_product, name='delete_product'),
    path('editproduct/<uuid:uid>',views.product_edit, name="product_edit"),
    path('addproduct',views.addproduct, name="addproduct"),
    
    path('variant/<uuid:uid>/',views.variant_show, name='variant'),
    path('edit_variant/<uuid:uid>/',views.edit_variant, name="edit_variant"),
    path('delete_variant/<uuid:uid>/',views.delete_variant, name="delete_variant"),
    
    path('image/<uuid:uid>',views.productimgage, name='productimage'),
    path('addimage/<uuid:uid>',views.addimage, name='addimage'),
    path('image_delete/<uuid:uid>',views.image_delete,name="image_delete"),
    
    path('brand/',views.brand, name='brand'),
    path('brand_edit/<int:id>/', views.brand_edit, name='brand_edit'),
    path('add_brand',views.add_brand, name='add_brand'),
    path('delete_brand/<int:id>/', views.delete_brand, name="delete_brand"),
    
    path('orderManegement/',views.orderManegement,name='orderManegement'),
    path('change_order_status/<uuid:uid>/',views.change_order_status, name="change_order_status"),
    path('single_order/<uuid:uid>/',views.single_order, name="single_order"),
    
    path('offers/',views.offers, name="offers"),
    path('edit_offers/<uuid:uid>/',views.edit_offers, name='edit_offers'),
    path('delete_offer/<uuid:uid>/', views.delete_offer, name="delete_offer"),
    
    path('coupon/', views.coupon, name='coupon'),
    path('edit_coupon/<uuid:uid>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<uuid:uid>/',views.delete_coupon, name='delete_coupon')

]