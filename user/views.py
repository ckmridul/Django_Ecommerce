from django.shortcuts import render, redirect
from account.models import Cart, CartItem
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from product.models import Coupon, Product, ProductVariant
from .models import Address, Wishlist, Wishlistitem
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from order.models import Order
from django.contrib.auth.decorators import login_required
import json
from base.session_key import session_key

# Create your views here.


def user_profile(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        image = request.FILES.get("image", None)

        user_obj = request.user
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.phone = phone
        if image:
            user_obj.profile_image = image
        user_obj.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, "profile/user_profile.html")


def change_password(request):
    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["password"]
        new1 = request.POST["password1"]

        if not request.user.check_password(old):
            messages.warning(request, "Invalid old password.")
            return redirect("userprofile")

        if new != new1:
            messages.warning(
                request, "New password and conform password shold be same!"
            )
            return redirect("userprofile")

        request.user.set_password(new)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Your password has been successfully changed.")
        return redirect("userprofile")
    return redirect("userprofile")


def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(is_paid=False, user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(
            is_paid=False, session_id=session_key(request)
        )

    cart_items = cart.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    if cart.coupon:
        total = total_price - cart.coupon.discount_price
        coupon_price = cart.coupon.discount_price

    else:
        total = total_price
        coupon_price = 0
    discount = round(
        sum(item.product.get_offer_price(item.variant) for item in cart_items), 2
    )
    total -= discount
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "cart": cart,
        "total": round(total, 2),
        "coupon_price": coupon_price,
        "discount": discount,
    }

    if request.method == "POST":
        coupon = request.POST.get("coupen")
        coupon_obj = Coupon.objects.filter(coupon_code=coupon)

        if not coupon_obj.exists():
            messages.warning(request, "Invalid Coupon")
            return HttpResponseRedirect(request.path_info)

        if cart.coupon:
            messages.warning(request, "Coupon already applied")
            return HttpResponseRedirect(request.path_info)

        if total_price < coupon_obj[0].minimum_amount:
            messages.warning(
                request, f"Amount should be grater than {coupon_obj[0].minimum_amount}"
            )
            return HttpResponseRedirect(request.path_info)

        if coupon_obj[0].is_expired:
            messages.warning(request, "Coupon expired")
            return HttpResponseRedirect(request.path_info)

        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request, "Coupon applied")
        return HttpResponseRedirect(request.path_info)

    return render(request, "profile/cart.html", context)


def update_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(is_paid=False, user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(
            is_paid=False, session_id=session_key(request)
        )

    cart_items = cart.cart_items.all()

    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data["uid"]
        Qty = data["quantity"]
        cart_item = CartItem.objects.get(uid=item_id)

        if int(Qty) > cart_item.variant.quantity:
            # messages.warning(request,'Out of stock')
            # return HttpResponseRedirect(request.path_info)

            error_message = "bla"  # Convert the error to a string
            return JsonResponse({"error": error_message}, status=400)

        if int(Qty) < 1:
            messages.warning(request, "Minimum quantity is 1")
            return HttpResponseRedirect(request.path_info)

        cart_item.quantity = Qty
        cart_item.save()
        quantity = cart_item.quantity
        price = cart_item.variant.price
        item_total = int(quantity) * int(price)
        total_price = sum(item.get_total_price() for item in cart_items)
        if cart.coupon:
            total = total_price - cart.coupon.discount_price
        else:
            total = total_price

        data = {"item_total": item_total, "sub_total": total_price, "total": total}
        return JsonResponse(data)


def delete_cart_item(request, uid):
    cart_item = CartItem.objects.get(uid=uid)
    cart_item.delete()
    return redirect("cart")


def remove_coupon(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon Removed")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def make_order(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.get(user=user)
        address = user.address.all()

    else:
        cart = Cart.objects.get(session_id=session_key(request))
        address = Address.objects.filter(session_id=session_key(request))
    cart_items = cart.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    if cart.coupon:
        total = total_price - cart.coupon.discount_price
        coupon_price = cart.coupon.discount_price
    else:
        total = total_price
        coupon_price = 0

    discount = round(
        sum(item.product.get_offer_price(item.variant) for item in cart_items), 2
    )
    total -= discount

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "total": total,
        "discount": discount,
        "coupon_price": coupon_price,
        "addresses": address,
    }
    return render(request, "product/order.html", context)


def add_address(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        pincode = request.POST["pincode"]
        place = request.POST["place"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        try:
            landmark = request.POST["landmark"]
            alternate_phone = request.POST["alternate_pnone"]
        except:
            landmark = None
            alternate_phone = None
        print(name)
        # save address
        if request.user.is_authenticated:
            user = request.user
            user_address = Address(
                user=user,
                name=name,
                landmark=landmark,
                city=city,
                pincode=pincode,
                state=state,
                place=place,
                address=address,
                phone=phone,
                alternate_number=alternate_phone,
            )
        else:
            user_address = Address(
                session_id=session_key(request),
                name=name,
                landmark=landmark,
                city=city,
                pincode=pincode,
                state=state,
                place=place,
                address=address,
                phone=phone,
                alternate_number=alternate_phone,
            )
        user_address.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def update_address(request, uid):
    user = request.user
    user_address = Address.objects.get(uid=uid)
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        pincode = request.POST["pincode"]
        place = request.POST["place"]
        address = request.POST["address"]
        city = request.POST["city"]
        state = request.POST["state"]
        try:
            landmark = request.POST["landmark"]
            alternate_phone = request.POST["alternate_phone"]
        except:
            landmark = None
            alternate_phone = None

        # Retrieve the user's address and update the fields
        user_address.name = name
        user_address.landmark = landmark
        user_address.city = city
        user_address.pincode = pincode
        user_address.state = state
        user_address.place = place
        user_address.address = address
        user_address.phone = phone
        if alternate_phone:
            user_address.alternate_number = alternate_phone
        user_address.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def myOrder(request):
    return render(request, "profile/orders.html")


def view_user_order(request, uid):
    order = Order.objects.get(uid=uid)
    orderItems = order.orderproduct.all()
    context = {"orderItems": orderItems, "order": order}
    return render(request, "profile/order_details.html", context)


def cancel_order(request, uid):
    order = Order.objects.get(uid=uid)
    order.status = "Cancelled"
    order.save()
    return redirect("myOrder")


def wishlist(request):
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    else:
        wishlist, _ = Wishlist.objects.get_or_create(session_id=session_key(request))

    return render(request, "profile/wishlist.html", {"wishlist": wishlist})


def add_wishlist(request, v_uid, p_uid):
    product = Product.objects.get(uid=p_uid)
    variant = ProductVariant.objects.get(uid=v_uid)
    if request.user.is_authenticated:
        user = request.user
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
    else:
        wishlist, _ = Wishlist.objects.get_or_create(session_id=session_key(request))

    wishlistitem = Wishlistitem(wishlist=wishlist, product=product, variant=variant)
    wishlistitem.save()

    messages.success(request, "wishlist added")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_wishlist(request, uid):
    item = Wishlistitem.objects.get(uid=uid)
    item.delete()
    return redirect("wishlist")


def add_to_cart_from_wish(request, uid):
    wish = Wishlistitem.objects.get(uid=uid)
    if request.user.is_authenticated:
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    else:
        cart, _ = Cart.objects.get_or_create(
            session_id=session_key(request), is_paid=False
        )
    if wish.variant.quantity < 1:
        messages.warning(request, "Out of Stock!")
        return HttpResponseRedirect(request.path_info)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=wish.product, variant=wish.variant
    )

    if not created:
        if cart_item.quantity == wish.variant.quantity:
            messages.warning(request, "out of stock")
            return HttpResponseRedirect(request.path_info)
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, "added succesfully")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
