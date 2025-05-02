from django.shortcuts import render
from .models import Packages
# Create your views here.


def home (request):
    packages=Packages.objects.all()
    
    return render(request,'index.html',context={"packages":packages})


def package_details(request,id):
    return render(request,'package-details.html')

def about_us(request):
    return render(request,'about.html')

def contact_us(request):
    return render(request,'contact.html')
