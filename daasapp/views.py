from imaplib import Time2Internaldate
from urllib import response
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import datetime
import json
import folium
import geocoder
# Create your views here.
date = datetime.datetime.now()
def generate(request):    
    districts = requests.get("http://127.0.0.1:8080/dbapi/district") 
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
        
        return redirect(report, sowing=response.text, harvesting=harvest_response.text, district=district)

    return render(request, "index.html", {
        "districts": districts.json
    })

def Homepage(request):    
    return render(request, "homepage.html")    

def chat(request):
    posts = requests.get("http://127.0.0.1:8080/dbapi/postmessage")
    replys = requests.get("http://127.0.0.1:8080/dbapi/replymessage")
    if request.method == "POST":
        message = request.POST.get('comment')
        # comment = request.POST['comment'] 
        # reply =request.POST.get('reply')      
        # reply_comment = request.POST['reply']
        print(message)
        data = {
            "user":1,
            "message":message
        }
        value1 = json.dumps(data)

        value2 = {
            "PostMessage": 2,
            "reply": message,            
        }
        requests.post("http://127.0.0.1:8080/dbapi/postmessage", data=value1) 
        # requests.post("http://127.0.0.1:8080/dbapi/replymessage", data=value2)      
        print(requests.post("http://127.0.0.1:8080/dbapi/postmessage", data=data) )
        messages.success(request, "Your comment has been posted successfully")
        
        return redirect(chat)
    # return redirect(f"/blog/{post.slug}")
    return render(request, "chat.html", {
            "posts": posts.json,
            "replys": replys.json
        })

def contact(request):
    if request.method == "POST":
        message = request.POST.get('message')
        comment = json.dumps({
            "user": 1,
            "comment": message
        })       

        requests.post("http://127.0.0.1:8080/dbapi/comment", data=comment)

        return redirect(Homepage)
    return render(request, "contact.html")

def login(request):
    return render(request, "login.html")

def report(request, sowing, harvesting, district):
    tmean = float(requests.get(f"http://127.0.0.1:8080/dbapi/weatherdetail/{date.year}/{date.month}/{date.day}/{district}").text)
    print(sowing, harvesting, tmean)  
    sow = None
    harvest = None
    if sowing == '[true]' and (tmean >= 15 and tmean <= 20):
        sow = True  
    else:
        sow = False  
    print(sow)
    if harvesting == '[true]' and tmean > 20:
        harvest = True
    else:
        harvest = False
    print(harvest)
    return render(request, "report.html", {
            "sowing": sow,
            "harvesting": harvest
        })   

def signup(request):
    return render(request, "signup.html")

def map(request):    
    location = geocoder.osm('Debre Elias')
    location2 = geocoder.osm("Debre Markos")
    location3 = geocoder.osm("Yejube")

    m = folium.Map(location=[9.1450, 40.4897], zoom_start=6)
    
    folium.Marker([location.lat, location.lng], tooltip="Debre Elias", popup=f"latitude - {location.lat}, longitude - {location.lng}").add_to(m)
    folium.Marker([location2.lat, location2.lng], tooltip="Debre Markos", popup=f"latitude - {location2.lat}, longitude - {location2.lng}").add_to(m)
    folium.Marker([location3.lat, location3.lng], tooltip="Yejube", popup=f"latitude -{location3.lat}, longitude - {location3.lng}").add_to(m)
    # folium.Marker([10.3296, 37.7344], tooltip="Debre Markos", popup=location.country).add_to(m)
    m = m._repr_html_()
    return render(request, "map.html", {
        "m": m
    })