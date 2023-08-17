from django.shortcuts import render
from product.models import Product,ProductVariant
from django.http import HttpResponseRedirect
from account.models import Cart,CartItem
from django.contrib import messages
from user.models import Wishlist,Wishlistitem
# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.get(slug =slug)
        variant = product.productVariant.first()
        p_offer = []
        c_offer = []

        if product.offer:
            p_price = variant.price - (variant.price * (product.offer.percentage / 100))
            p_offer = [p_price,product.offer]
            print(p_price)
            
        if product.category.offer:
            c_price = variant.price - (variant.price * (product.category.offer.percentage / 100))
            c_offer = [c_price,product.category.offer]
            print(c_price)
            
        if p_offer and c_offer:
            price = min(p_offer,c_offer)
        elif p_offer and not c_offer:
            price = p_offer
        elif not p_offer and c_offer:
            price = c_offer
        else:
            price =None
        print(price)
            
        context = {'product' : product,
                   'selected_ram': product.productVariant.first().ram,
                   'selected_variant' : variant,
                   'price': price
                   }
        
        if request.GET.get('ram'):
            ram = request.GET.get('ram')
            variant = product.get_variants_by_ram(ram)
            if product.offer:
                p_price = variant.price - (variant.price * (product.offer.percentage / 100))
                p_offer = [p_price,product.offer]
                print(p_price)
            
            if product.category.offer:
                c_price = variant.price - (variant.price * (product.category.offer.percentage / 100))
                c_offer = [c_price,product.category.offer]
                print(c_price)
                    
            if p_offer and c_offer:
                price = min(p_offer,c_offer)
            elif p_offer and not c_offer:
                price = p_offer
            elif not p_offer and c_offer:
                price = c_offer
            else:
                price =None
            print(price)
     
            context['selected_ram'] = ram
            context['selected_variant'] = variant
            context['price'] = price
            
            
        
        
        wishlist = Wishlist.objects.get(user = request.user)
        wishlistitem = Wishlistitem.objects.filter(wishlist = wishlist, product = product, variant = context['selected_variant'])
        if wishlistitem:
            context['wish'] = True
            print
        else:
            context['wish'] = False
        return render(request, 'product/product.html', context)
    
    except Exception as e:
        print(e)
        
        return render(request, 'product/product.html', context)
    
        
def session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key



def add_to_cart(request, uid):
   
    variant_id = request.GET.get('variant')
    
    product = Product.objects.get(uid = uid)
    if request.user.is_authenticated:
        user = request.user
        cart , _ = Cart.objects.get_or_create(user = user, is_paid = False)
    else:
        cart , _ = Cart.objects.get_or_create(session_id = session_key(request), is_paid = False)
        
    if variant_id:
        
        variant = ProductVariant.objects.get(uid = variant_id)
        cart_item,created = CartItem.objects.get_or_create(cart=cart, product=product,variant=variant)
        if not created:
            if cart_item.quantity > variant.quantity:
                messages.warning(request, 'out of stock')
                return HttpResponseRedirect(request.path_info)
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, 'added succesfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

