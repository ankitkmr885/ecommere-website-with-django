from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from system.models import signup
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="login")
def home(request):
    return HttpResponse("this is homepage")

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
        # get the post parameter
        username= request.POST["loginusername"]
        password= request.POST["loginpassword"]
        # aunthenticate valid user
        user = authenticate(username=username,password=password)
        # if user id and password are entered wrong by client
        if user is not None:
            login(request, user)
           
            return (render(request, 'home.html'))
        else:
            messages.error(request,"invalid credentials,please try again")
            return redirect("homepage")

    return (render(request, 'login.html'))

    # logout function
def logout_page(request):
    logout(request)
    messages.success(request, "sucessfully logout")
    return redirect('loginpage')
