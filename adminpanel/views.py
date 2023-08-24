import json
from django.shortcuts import render, redirect
from account.models import Profile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from product.models import (
    Product,
    Brand,
    Category,
    Productimage,
    Offer,
    Coupon,
    ProductVariant,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from .forms import ImageForm
from django.core.paginator import Paginator
from order.models import Order
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from openpyxl import Workbook

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminpanel(request):
    if not request.user.is_superuser:
        return redirect("adminlogin")

    selected_value = request.GET.get("selected_value")
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year
    current_week = current_date.isocalendar()[1]
    current_day = timezone.now().date()
    user_type = []
    revenue_year = Order.objects.filter(
        created_at__year=current_year, status="Delivered"
    ).aggregate(total=Sum("order_total"))["total"]

    revenue_month = Order.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month,
        status="Delivered",
    ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"] or 0

    revenue_week = Order.objects.filter(
        created_at__year=current_year,
        created_at__month=current_month,
        created_at__week=current_week,
        status="Delivered",
    ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]

    revenue_day = Order.objects.filter(
        created_at__date=current_day, status="Delivered"
    ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]

    gust_count = Order.objects.filter(user__isnull=True, is_orderd=True).count()

    user_type.append(gust_count)

    user_count = Order.objects.filter(user__isnull=False, is_orderd=True).count()
    user_type.append(user_count)

    if selected_value == "month":
        # for chart
        # Create a list to hold total prices for each month
        monthly_total_prices = []
        previous = []
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        # Iterate through each month (from January to December)
        for month_number in range(1, 13):
            total_price_curr = (
                Order.objects.filter(
                    created_at__month=month_number,
                    status="Delivered",
                    created_at__year=current_year,
                ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]
                or 0
            )

            total_price_pre = (
                Order.objects.filter(
                    created_at__month=month_number,
                    status="Delivered",
                    created_at__year=(current_year - 1),
                ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]
                or 0
            )

            total_price_float_curr = float(total_price_curr)
            monthly_total_prices.append(total_price_float_curr / 1000)

            total_price_float_pre = float(total_price_pre)
            previous.append(total_price_float_pre / 1000)

        data = {
            "current": monthly_total_prices,
            "previous": previous,
            "previousstr": "previous year",
            "currentstr": "current year",
            "revenue": revenue_year,
            "category": months,
        }
        return JsonResponse(data)

    if selected_value == "year":
        yearly_total_prices = []
        year = [(current_year - 10) + i for i in range(11)]

        for year_number in year:
            total_price_curr = (
                Order.objects.filter(
                    created_at__year=year_number,
                    status="Delivered",
                ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]
                or 0
            )

            total_price_float_curr = float(total_price_curr)
            yearly_total_prices.append(total_price_float_curr / 1000)

        data = {
            "current": yearly_total_prices,
            "previous": None,
            "previousstr": None,
            "currentstr": "current week",
            "revenue": revenue_month,
            "category": year,
        }
        return JsonResponse(data)

    current_date = datetime.now()
    start_date = current_date - timedelta(days=14)
    daily_total = []

    while start_date <= current_date:
        daily_total_price = (
            Order.objects.filter(
                created_at__date=start_date, status="Delivered"
            ).aggregate(total_price_sum=Sum("order_total"))["total_price_sum"]
            or 0
        )

        daily_total_price_float = float(daily_total_price)
        daily_total.append(daily_total_price_float)

        start_date += timedelta(days=1)

    month = current_date.strftime("%b")

    monthly = json.dumps(daily_total)
    total_order = Order.objects.filter(is_orderd=True).count()
    user_type_json = json.dumps(user_type)
    context = {
        "user_type": user_type_json,
        "total_order": total_order,
        "monthly": monthly,
        "revenue_month": round(revenue_month, 2),
        "current_month": month,
    }

    return render(request, "adminpanel/dashboard.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def userMange(request):
    user1 = Profile.objects.all()

    paginator = Paginator(user1, 3)
    page_number = request.GET.get("page")
    user = paginator.get_page(page_number)
    return render(request, "adminpanel/usermanage/usermanagement.html", {"users": user})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def blockUser(request, id):
    user = Profile.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def catagoryManage(request):
    categories = Category.objects.all()
    offers = Offer.objects.all()

    context = {"categories": categories, "offers": offers, "null": 0}

    return render(request, "adminpanel/category.html", context)



def add_category(request):
    if request.method == "POST":
        name = request.POST["category_name"]
        image = request.FILES.get("image")
        cat = Category.objects.filter(category_name = name)
        if cat:
            messages.warning(request, "category name already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        if request.POST["offer"] == "0":
            off = int(request.POST["offer"])
            offer_id = bool(off)

        else:
            offer_id = request.POST["offer"]
        if offer_id:
            offer = Offer.objects.get(uid=offer_id)
        else:
            offer = None
            
        Category.objects.create(category_name = name, category_image=image, offer = offer)
        
    return redirect("catagory")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def editcategory(request, uid):
    if request.method == "POST":
        name = request.POST["category_name"]
        caterg = Category.objects.get(uid=uid)

        try:
            image = request.FILES.get("image")

        except:
            image = None
            
        cat = Category.objects.filter(category_name = name)
        if cat:
            messages.warning(request, "category name already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if request.POST["offer"] == "0":
            off = int(request.POST["offer"])
            offer_id = bool(off)

        else:
            offer_id = request.POST["offer"]
        if offer_id:
            offer = Offer.objects.get(uid=offer_id)
        else:
            offer = None
        if image:
            caterg.category_image = image
        caterg.category_name = name
        caterg.offer = offer
        caterg.save()

        return redirect("catagory")


def delete_catagory(request,uid):
    catagory = Category.objects.get(uid = uid)
    catagory.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="adminlogin")
def productview(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    product = Product.objects.all()
    catagory = Category.objects.all()
    brand = Brand.objects.all()
    offers = Offer.objects.all()

    paginator = Paginator(product, 3)
    page_number = request.GET.get("page")
    productfinal = paginator.get_page(page_number)

    context = {
        "product": productfinal,
        "catagory": catagory,
        "brands": brand,
        "offers": offers,
        "null": 0,
    }
    return render(request, "adminpanel/product.html", context)


def product_edit(request, uid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST["product_name"]
        brand = request.POST["brand"]
        category_id = request.POST.get("category")
        product_description = request.POST.get("product_description")
        pro = Product.objects.filter(product_name = name)
        if pro:
            messages.warning(request, "category name already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        if request.POST["offer"] == "0":
            off = int(request.POST["offer"])
            offer_id = bool(off)
        else:
            offer_id = request.POST["offer"]

        brand_obj = Brand.objects.get(id=brand)
        category_obj = Category.objects.get(uid=category_id)

        if offer_id:
            offer = Offer.objects.get(uid=offer_id)
        else:
            offer = None

        editproduct = Product.objects.get(uid=uid)
        editproduct.product_name = name
        editproduct.brand = brand_obj
        editproduct.category = category_obj
        editproduct.product_description = product_description
        editproduct.offer = offer
        editproduct.save()

    messages.success(request, "product edited successfully!")
    return redirect("product_view")


@login_required(login_url="admin_login")
def addproduct(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST["product_name"]
        brand = request.POST["brand"]
        category_id = request.POST.get("category")
        product_description = request.POST.get("product_description")
        
        pro = Product.objects.filter(product_name = name)
        if pro:
            messages.warning(request, "category name already exists")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        
        if request.POST["offer"] == "0":
            off = int(request.POST["offer"])
            offer_id = bool(off)
        else:
            offer_id = request.POST["offer"]

        # Validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, "Product name already exists")
            return redirect("product")

        brand_obj = Brand.objects.get(id=brand)
        category_obj = Category.objects.get(uid=category_id)
        if offer_id:
            offer = Offer.objects.get(uid=offer_id)
        else:
            offer = None

        # Save

        product = Product(
            product_name=name,
            category=category_obj,
            product_description=product_description,
            brand=brand_obj,
            offer=offer,
        )

        # else:
        #     product = Product(
        #         product_name=name,
        #         category=category_obj,
        #         product_description=product_description,
        #         brand=brand_obj
        # )

        product.save()
        messages.success(request, "product added successfully!")
        return redirect("product_view")
    return redirect("product_view")


def delete_product(request, uid):
    product = Product.objects.get(uid=uid)
    if product.status:
        product.status = False
    else:
        product.status = True
    product.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def productimgage(request, uid):
    product = Product.objects.get(uid=uid)
    images = Productimage.objects.filter(product=product)
    context = {"images": images, "product_id": uid}

    return render(request, "adminpanel/productmanage/image.html", context)


def addimage(request, uid):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        product = Product.objects.get(uid=uid)

        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.product = product
            image_instance.save()

            return JsonResponse({"message": "works", "img_id": uid})

        else:
            print("Form is not valid:", form.errors)

    else:
        form = ImageForm()

    context = {"form": form, "img_id": uid}
    return render(request, "adminpanel/productmanage/add_image.html", context)


def image_delete(request, uid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    try:
        delete_image = Productimage.objects.get(uid=uid)
        delete_image.delete()
        product = delete_image.product
        images = Productimage.objects.filter(product=product)
        context = {"images": images, "product_id": uid}
        messages.success(request, "image deleted successfully!")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    except:
        return redirect("productimage")


def brand(request):
    brand1 = Brand.objects.all()
    paginator = Paginator(brand1, 3)
    page_number = request.GET.get("page")
    brand = paginator.get_page(page_number)
    return render(request, "adminpanel/productmanage/brand.html", {"brands": brand})


def brand_edit(request, id):
    if request.method == "POST":
        brand = Brand.objects.get(id=id)
        name = request.POST["name"]
        try:
            image = request.FILES.get("image")
            brand.title = name
            brand.image = image

        except:
            brand.title = name
        brand.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_brand(request):
    if request.method == "POST":
        name = request.POST["name"]
        image = request.FILES.get("image")
        Brand.objects.create(title=name, image=image)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_brand(request, id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def orderManegement(request):
    order1 = Order.objects.all()
    paginator = Paginator(order1, 5)
    page_number = request.GET.get("page")
    order = paginator.get_page(page_number)

    context = {"orders": order}
    return render(request, "adminpanel/order.html", context)


def change_order_status(request, uid):
    if request.method == "POST":
        order = Order.objects.get(uid=uid)
        status = request.POST.get("status")
        order.status = status
        order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def single_order(request, uid):
    order = Order.objects.get(uid=uid)
    orderItems = order.orderproduct.all()
    context = {"orderItems": orderItems, "order": order}
    return render(request, "adminpanel/single_order.html", context)


def offers(request):
    offers = Offer.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        discount = request.POST["discount"]

        Offer.objects.create(name=title, percentage=discount)
    context = {"offers": offers}
    return render(request, "adminpanel/productmanage/offers.html", context)


def edit_offers(request, uid):
    offer = Offer.objects.get(uid=uid)
    if request.method == "POST":
        title = request.POST["title"]
        discount = request.POST["discount"]

        offer.name = title
        offer.percentage = discount
        offer.save()

    return redirect("offers")


def delete_offer(request, uid):
    Offer.objects.get(uid=uid).delete()
    return redirect("offers")


def coupon(request):
    if request.method == "POST":
        code = request.POST["code"]
        minimun = request.POST["minimum"]
        price = request.POST["price"]
        Coupon.objects.create(
            coupon_code=code, discount_price=price, minimum_amount=minimun
        )

    context = {"coupons": Coupon.objects.all()}
    return render(request, "adminpanel/productmanage/coupon.html", context)


def edit_coupon(request, uid):
    coupon = Coupon.objects.get(uid=uid)
    if request.method == "POST":
        code = request.POST["code"]
        minimun = int(request.POST["minimum"])
        price = int(request.POST["price"])

        coupon.coupon_code = code
        coupon.minimum_amount = minimun
        coupon.discount_price = price
        coupon.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_coupon(request, uid):
    coupon = Coupon.objects.get(uid=uid)
    coupon.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def variant_show(request, uid):
    product = Product.objects.get(uid=uid)
    variant = product.productVariant.all()
    if request.method == "POST":
        quantity = request.POST["quantity"]
        color = request.POST["color"]
        price = request.POST["price"]
        ram = request.POST["ram"]
        storage = request.POST["storage"]

        ProductVariant.objects.create(
            product=product,
            quantity=quantity,
            color=color,
            price=price,
            ram=ram,
            storage=storage,
        )

    context = {"variants": variant, "product_id": uid}
    return render(request, "adminpanel/productmanage/variant.html", context)


def edit_variant(request, uid):
    variant = ProductVariant.objects.get(uid=uid)

    if request.method == "POST":
        quantity = request.POST["quantity"]
        color = request.POST["color"]
        price = request.POST["price"]
        ram = request.POST["ram"]
        storage = request.POST["storage"]

        variant.quantity = quantity
        variant.color = color
        variant.price = price
        variant.ram = ram
        variant.storage = storage

        variant.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_variant(request, uid):
    ProductVariant.objects.get(uid=uid).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def sales_report(request):
    if request.method == "POST":
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        format = request.POST["format"]
        if start_date != end_date:
            orders = Order.objects.filter(
                status="Delivered", created_at__range=(start_date, end_date)
            )
        else:
            orders = Order.objects.filter(
                status="Delivered", created_at__date=start_date
            )

        if format == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'
            doc = SimpleDocTemplate(response, pagesize=A4)
            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )

            data = [
                [
                    "Sl",
                    "Order Number",
                    "User Email",
                    "Payment Method",
                    "Order Total",
                    "Created Date",
                ]
            ]
            counter = 1
            for order in orders:
                user_email = order.user.email if order.user else "Guest User"
                created_date = order.created_at.strftime("%d-%m-%Y %I:%M %p")
                data.append(
                    [
                        counter,
                        order.order_number,
                        user_email,
                        order.payment.payment_method,
                        order.order_total,
                        created_date,
                    ]
                )
                counter += 1
            table = Table(data)
            table.setStyle(table_style)

            # Build the PDF document
            elements = []
            styles = getSampleStyleSheet()
            elements.append(Paragraph("Sales Report", styles["Title"]))
            elements.append(table)

            doc.build(elements)

            return response

        if format == "excel":
            output = io.BytesIO()
            wb = Workbook()
            ws = wb.active
            headers = [
                "Sl",
                "Order Number",
                "User Email",
                "Payment Method",
                "Order Total",
                "Created Date",
            ]
            ws.append(headers)

            counter = 1
            for order in orders:
                user_email = order.user.email if order.user else "Guest User"
                created_date = order.created_at.strftime("%d-%m-%Y %I:%M %p")
                row_data = [
                    counter,
                    order.order_number,
                    user_email,
                    order.payment.payment_method,
                    order.order_total,
                    created_date,
                ]
                ws.append(row_data)
                counter += 1

            wb.save(output)
            output.seek(0)

            # Create an HTTP response with the Excel file
            response = HttpResponse(
                output.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = 'attachment; filename="sales_report.xlsx"'

            return response
