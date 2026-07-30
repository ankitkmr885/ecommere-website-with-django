from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from home.models import CartItem


@login_required(login_url="loginpage")
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email=request.POST.get("email")
        pass1= request.POST.get("password")
        pass2= request.POST.get("password2")
        


# name should must be under 10 character.
        if len(name) > 20:
            messages.error(request, "username mustbe under 20 character")
            return redirect("signup_page")


# name should contain only letter and number.
        if not name.isalnum():
            messages.error(request, "username should only contain letter and no.")
            return redirect("signup_page")

# to check username from the database if there is already present then through an error
        if User.objects.filter(username = name):
            messages.error(request, "This username is already taken")
            return redirect("signup_page")
         
        
# to check password or confirm password must be same

        if pass1!=pass2:
            messages.error(request, "your password & confirm password are not matched")
            return redirect("signup_page")
        
# create the user.
        else:
            my_user = User.objects.create_user(name,email,pass1)
            my_user.save()
            messages.success(request, 'user created sucessfully! please go through login!!')
            return redirect("signup_page")
    return (render(request, 'signup.html'))

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("loginusername")
        password = request.POST.get("loginpassword")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            cart = request.session.get("cart", {})
            if cart:
                for product_id, quantity in cart.items():
                    product = None
                    try:
                        from home.models import Product
                        product = Product.objects.get(pk=int(product_id))
                    except (ValueError, Product.DoesNotExist):
                        continue

                    item, created = CartItem.objects.get_or_create(user=user, product=product)
                    if not created:
                        item.quantity += int(quantity)
                    else:
                        item.quantity = int(quantity)
                    item.save()

                request.session["cart"] = {}

            return redirect("home")
        else:
            messages.error(request, "invalid credentials,please try again")
            return redirect("loginpage")

    return render(request, "login.html")

    # logout function
def logout_page(request):
    logout(request)
    messages.success(request, "sucessfully logout")
    return redirect('loginpage')

# forget function
def forget(request):
    return (render(request, 'forgetpass.html'))

# change pass for forget function
def changepass(request):
    return render(request, 'changepass.html')
