from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from home.models import CartItem, Order, OrderItem, Product, SellerProfile, contact


def get_cart_count(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).count()
    return len(request.session.get("cart", {}))


def get_seller_profile(user):
    return getattr(user, "seller_profile", None)


def index(request):
    products = Product.objects.filter(active=True).order_by("-created_at")
    context = {"variable": "this is sent", "products": products, "cart_count": get_cart_count(request)}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html", {"cart_count": get_cart_count(request)})


def services(request):
    return render(request, "services.html", {"cart_count": get_cart_count(request)})


def contactUser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        description = request.POST.get("description")
        contact1 = contact(name=name, email=email, phone=phone, description=description, date=datetime.today())
        contact1.save()
        messages.success(request, "your messages has been submited sucessfully!")
    return render(request, "contact.html", {"cart_count": get_cart_count(request)})


def seller_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        shop_name = request.POST.get("shop_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken")
            return redirect("seller_register")

        user = User.objects.create_user(username=username, email=email, password=password)
        SellerProfile.objects.create(user=user, shop_name=shop_name, phone=phone, address=address)
        login(request, user)
        messages.success(request, "Seller account created successfully")
        return redirect("seller_dashboard")

    return render(request, "seller_register.html", {"cart_count": get_cart_count(request)})


@login_required(login_url="loginpage")
def seller_dashboard(request):
    profile = get_seller_profile(request.user)
    if not profile:
        messages.error(request, "Create a seller profile first")
        return redirect("seller_register")

    products = profile.products.all().order_by("-created_at")
    orders = Order.objects.filter(seller=profile).order_by("-created_at")
    return render(
        request,
        "seller_dashboard.html",
        {"profile": profile, "products": products, "orders": orders, "cart_count": get_cart_count(request)},
    )


@login_required(login_url="loginpage")
def add_product(request):
    profile = get_seller_profile(request.user)
    if not profile:
        messages.error(request, "Create a seller profile first")
        return redirect("seller_register")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.POST.get("image", "")
        if name and price:
            Product.objects.create(seller=profile, name=name, description=description, price=price, image=image)
            messages.success(request, "Product added successfully")
            return redirect("seller_dashboard")

    return render(request, "add_product.html", {"cart_count": get_cart_count(request)})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)

    if request.user.is_authenticated:
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.quantity += 1
            item.save()
        else:
            item.quantity = 1
            item.save()
        messages.success(request, f"{product.name} added to your cart")
    else:
        cart = request.session.get("cart", {})
        cart[str(product_id)] = int(cart.get(str(product_id), 0)) + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} added to your cart")

    return redirect("cart")


@login_required(login_url="loginpage")
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total": total, "cart_count": get_cart_count(request)})


@login_required(login_url="loginpage")
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect("cart")


@login_required(login_url="loginpage")
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")
    if not cart_items:
        messages.info(request, "Your cart is empty")
        return redirect("cart")

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        if not address or not phone:
            messages.error(request, "Please enter shipping address and phone")
            return redirect("checkout")

        sellers = {item.product.seller for item in cart_items}
        created_orders = []
        for seller in sellers:
            seller_items = [item for item in cart_items if item.product.seller_id == seller.id]
            order = Order.objects.create(
                buyer=request.user,
                seller=seller,
                shipping_address=address,
                phone=phone,
                payment_status="paid",
            )
            for item in seller_items:
                OrderItem.objects.create(order=order, product=item.product, seller=seller, quantity=item.quantity, price=item.product.price)
            created_orders.append(order)

        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, "Payment successful. Your order is now pending seller approval.")
        if created_orders:
            return redirect("order_tracking", order_id=created_orders[0].id)
        return redirect("my_orders")

    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "checkout.html", {"cart_items": cart_items, "total": total, "cart_count": get_cart_count(request)})


@login_required(login_url="loginpage")
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders, "cart_count": get_cart_count(request)})


@login_required(login_url="loginpage")
def order_tracking(request, order_id):
    order = get_object_or_404(Order, pk=order_id, buyer=request.user)
    return render(request, "order_tracking.html", {"order": order, "cart_count": get_cart_count(request)})


@login_required(login_url="loginpage")
def update_order_status(request, order_id, status):
    profile = get_seller_profile(request.user)
    if not profile:
        return redirect("seller_register")

    order = get_object_or_404(Order, pk=order_id, seller=profile)
    order.status = status
    order.save()
    messages.success(request, "Order status updated")
    return redirect("seller_dashboard")
