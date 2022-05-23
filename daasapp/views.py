from imaplib import Time2Internaldate
from urllib import response
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
# Create your views here.

def generate(request):
    date = datetime.datetime.now()
    districts = requests.get("http://127.0.0.1:8080/dbapi/district")
    ds = W
    # tmin = requests.get("http://127.0.0.1:8080/dbapi/weather").json
    # tmax = requests.get("http://127.0.0.1:8080/dbapi/weather").json
    value = {
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "tmax": 15.1
    }
    value2 = {
        "year": 2017,
        "month": 12,
        "day": 127,
        "tmin": 5.4,
        "tmax": 23.3
    }
    if request.method == 'POST':
        district = request.POST['District']
        print(district)
        response = requests.post("http://127.0.0.1:8080/api/" + district + '/', data=value)
        harvest_response = requests.post("http://127.0.0.1:8080/api/harvest_" + district + '/', data=value2)
        print(response.text, harvest_response.text)
        
        return redirect(report, sowing=response.text, harvesting=harvest_response.text)


    return render(request, "index.html", {
        "districts": districts.json
    })

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

def report(request, sowing, harvesting):
    print(sowing, harvesting)
    if sowing == '[true]' and harvesting == "[true]":
        return render(request, "report.html", {
            "sowing": "True",
            "harvesting": "True"
        }) 
    elif sowing == "[false]" and harvesting == "[true]":
        return render(request, "report.html", {
            "sowing": "False",
            "harvesting": "True"
        }) 
    elif sowing == "[true]" and harvesting == "[false]":
        return render(request, "report.html", {
            "sowing": "True",
            "harvesting": "False"
        }) 
    elif sowing == "[false]" and harvesting == "[false]":
        return render(request, "report.html", {
            "sowing": "False",
            "harvesting": "False"
        }) 

def signup(request):
    return render(request, "signup.html")