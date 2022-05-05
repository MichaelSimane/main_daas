from urllib import response
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def generate(request):
    value = {
        "year": 2022,
        "month": 2,
        "day": 11,
        "tmax": 27.6
    }
    if request.method == 'POST':
        district = request.POST['District']
        if district == "Yejubie":
            response = requests.post("http://127.0.0.1:8080/api/rainYJ/", data=value)
            # return render(request, "report.html",  {
            #     'sowing': response.json
            # })
            print(response.text)
            if response.text == '[true]':
                sowing = 1
                return redirect(report, sowing=sowing)
            else:
                sowing = 0
                return redirect(report, sowing=sowing)

    return render(request, "index.html")

def Homepage(request):
    value = {
        "year": 2023,
        "month": 7,
        "day": 3,
        "tmax": 18.4
    }
    
    response = requests.post("http://127.0.0.1:8080/api/rain/", data=value)
    print(response.status_code)
    # return HttpResponseRedirect(reverse("report", args=(response.content)))
    return render(request, "homepage.html", {
        "rain": response.text
    })    

def chat(request):
    return render(request, "chat.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
    return render(request, "login.html")

def report(request, sowing):
    if sowing ==  1:
        return render(request, "report.html", {
            "sowing": "True"
        }) 
    else:
        return render(request, "report.html", {
            "sowing": "False"
        }) 

def signup(request):
    return render(request, "signup.html")