from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile,Cart
import random
from base.emails import send_account_activation_email




            
def session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key




def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.session.session_key:
        cart_gust = Cart.objects.get(session_id = request.session.session_key)
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = Profile.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, "Account not found!")
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].is_email_verified:
            messages.warning(request, "Your account is not verified")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(request, username=email, password=password)

        if user_obj:
            login(request, user_obj)
            
            if cart_gust:
                cart,_ = Cart.objects.get_or_create(user = request.user)
                gust_items = cart_gust.cart_items.all()
                
                for gust_item in gust_items:
                    gust_item.cart = cart
                    gust_item.save()
                    
                cart_gust.delete()
                
            return redirect("/")
        messages.warning(request,'Password does not match')

    return render(request, "account/login.html")


def register(request):
    if request.method == "POST":
        try:
            get_otp = request.POST.get("otp")
        except:
            get_otp = None

        if get_otp:
            email = request.POST.get("email")
            user_obj = get_object_or_404(Profile, email=email)
            session_otp = request.session.get('otp')
            print(type(session_otp))
            print(get_otp)
            if session_otp == int(get_otp):
                user_obj.is_email_verified = True
                user_obj.save()
                del request.session['otp']
                return redirect("login_page")
            
            context = {
                "otp": True,
                "message": messages.warning(request, "Invalid OTP"),
                "email" :email
               
            }
            return render(request, "account/register.html", context)

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        phone = request.POST.get("phone")

        user_obj = Profile.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(request.path_info)

        user_obj = Profile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            phone=phone,
        )
        user_obj.set_password(password)
        email_otp = random.randint(100000, 999999)
        request.session['otp'] = email_otp
        user_obj.save()

        send_account_activation_email(email, email_otp)

        context = {
            "otp": True,
            "message": messages.success(request, "An email has been sent to your mail"),
            "name": first_name,
            "email" :email
        }

        return render(request, "account/register.html", context)

    return render(request, "account/register.html")


def activate_email(request, email_otp):
    try:
        user = get_object_or_404(Profile, email_otp=email_otp)
        user.is_email_verified = True
        user.save()
        return redirect("login_page")
    except Profile.DoesNotExist:
        messages.warning(request, "Invalid OTP!")
        return HttpResponseRedirect(request.path_info)


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('adminpanel')

    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_obj = Profile.objects.filter(username=email)

        if not user_obj.exists():
            messages.warning(request, "Account not found!")
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].is_superuser:
            messages.warning(request, "You can't access this site")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(request, username=email, password=password)

        if user_obj:
            login(request, user_obj)
            return redirect("/admindashboard/")

    return render(request, "account/adminlogin.html")

def logout_page(request):
    logout(request)
    return redirect('/')



def forgot_password(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
        except:
            email = None
        try:
            get_otp = request.POST['otp']
        except:
            get_otp = None
        try:
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
        except:
            pass1 = None
            pass2 = None
            
            
        if get_otp:
            session_otp = request.session.get('otp')
            print(type(session_otp))
            print(get_otp)
            if session_otp == int(get_otp):
                del request.session['otp']
                return render(request,'account/forgot_password.html',{'email':email})
            
            messages.warning(request,'Invalid Otp')
            return HttpResponseRedirect(request.path_info)
        if pass1:
            if pass1 == pass2:
                print(email,'jj')
                user_obj= Profile.objects.get(email=email)
                user_obj.set_password(pass1)
                user_obj.save()
                return redirect('login_page')
            messages.warning(request,'password should match')
        
        
        if email:
            try:
                user_obj = Profile.objects.get(email=email)
            except:
                user_obj = None
            if user_obj:
                email_otp = random.randint(100000, 999999)
                print(email_otp)
                request.session['otp'] = email_otp
                send_account_activation_email(email, email_otp)
                return render(request,'account/forgot_password.html',{'otp':True,'email':email})
            messages.warning(request,'Invalid User')
            return HttpResponseRedirect(request.path_info)

            
    return render(request,'account/forgot_password.html',{'em':True})
    