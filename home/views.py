from django.shortcuts import render,HttpResponse
from datetime import datetime
from home.models import contact
from django.contrib import messages

# Create your views here.
def index(request):
    context={
        "variable":"this is sent"
    }
    return render(request,'index.html',context)
    # return HttpResponse("this is homepage")

def about(request):
    return render(request,'about.html')
    # return HttpResponse("this is aboutpage")

def services(request):
     return render(request,'services.html')
    # return HttpResponse("this is servicespage")

def contactUser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        description = request.POST.get("description")
        contact1 = contact(name=name, email=email, phone=phone, description=description, date = datetime.today())
        contact1.save()
        messages.success(request, 'your messages has been submited sucessfully!')
    return render(request,'contact.html')
    # return HttpResponse("this is contactpage")
