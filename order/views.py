from django.shortcuts import render,redirect
from account.models import CartItem, Cart
from .models import Order,Payment,OrderProduct
from user.models import Address
import random,time
import razorpay,json
from django.conf import settings
from django.http import JsonResponse


# Create your views here.



def get_payment_details(pid):
  payment_id = pid
  client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
  payment_obj = client.payment.fetch(payment_id)
  return payment_obj


def payment(request):
    
    body = json.loads(request.body)
    print(body)
    OrdID = body['OrdID']
    order = Order.objects.get(user = request.user, is_orderd = False, order_number = OrdID)
    pid = body['PayID']
    payment_details = get_payment_details(pid)
    payment = Payment(
        user = request.user,
        payment_id = payment_details['id'],
        payment_method = payment_details['method'],
        amount_paid = order.order_total,
        status = payment_details['status'])
    print(payment)
    payment.save()
    order.payment = payment
    order.is_orderd = True
    order.status = 'Order Placed'
    order.save()
    
    #cartItems to order item
    cart = Cart.objects.get(user = request.user)
    cartItems = cart.cart_items.all()
    for item in cartItems:
        order_product = OrderProduct(
            order = order,
            product = item.product,
            variation = item.variant,
            quantity = item.quantity,
            
        )
        order_product.save()
        variant = item.variant
        variant.quantity -= item.quantity
        variant.save()
    cart.delete()
         
    data = {
        'order_number': OrdID,
        'transID':pid
    }
    
    
    return JsonResponse(data)




def place_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart = cart)
    total_price = sum(item.get_total_price() for item in cart_items)
    discount = sum(item.product.get_offer_price(item.variant) for item in cart_items)
    
    if not cart_items.exists():
        return redirect('/')
    
    
    if cart.coupon:
        total = total_price - cart.coupon.discount_price
        coupon_price = cart.coupon.discount_price
    else:
        total = total_price
        coupon_price = 0
    
    total -= discount
    
    
    if request.method == 'POST':
        address_id = request.POST['address']
        timestamp = int(time.time())
        random_number = random.randint(1000, 9999)
        order_number = f"ORD-{timestamp}-{random_number}"
        address = Address.objects.get(uid=address_id)
        order = Order(
            user=user,
            order_total=total,
            address=address,
            order_number=order_number,
            coupon_price = coupon_price,
            subtotal = total_price,
            discount = discount
            
        )
        order.save()
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount':int(total), 'currency': 'INR', 'payment_capture': 1})
        
        print(payment,'trtt')
        
        context = {
            'payment':payment,
            'order':order,
            'cart_items':cart_items,
            'total_price':total_price,
            'total':total,
            'coupon_price':coupon_price,
            'address':address,
            'discount':discount
            
        }
        
        return render(request,'product/payment.html', context)
    return redirect('make_order')
    

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    
    try:
        order = Order.objects.get(order_number=order_number, is_orderd = True)
        order_products = OrderProduct.objects.filter(order = order)
        payment = Payment.objects.get(payment_id = transID)
        
        context = {
            'order':order,
            'order_products':order_products,
            'transID':payment.payment_id,
            'payment':payment
        }
        
        return render(request, 'product/order_complete.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('index')