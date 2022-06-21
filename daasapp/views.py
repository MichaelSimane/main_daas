from imaplib import Time2Internaldate
from urllib import response
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
import datetime
from dateutil.relativedelta import relativedelta
import json
import folium
import geocoder
from selenium import webdriver
from django.contrib.auth import authenticate, login, logout
from django.forms import ValidationError
from .models import DAAS_User
from .forms import UserLogin, UserRegister
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
        locust_response = requests.post("http://127.0.0.1:8080/api/locust_" + district + '/', data=value)
        print(response.text, harvest_response.text)
        
        return redirect(report, sowing=response.text, harvesting=harvest_response.text, locust=locust_response.text, district=district)

    return render(request, "index.html", {
        "districts": districts.json
    })

def detailReport(request, year, month, district, sowing, harvesting, locust):      
    print(district)        
    soil_response = requests.get("http://127.0.0.1:8080/dbapi/soildetail/" + district)
    weather_response = requests.get(f"http://127.0.0.1:8080/dbapi/WeatherDetailReportApi/{year}/{month}/{district}")
    # print(response.text, harvest_response.text)
    soil = json.loads(soil_response.text)
    print(soil['type'])
    four_months = date.today() + relativedelta(months=+4)
    print(four_months.strftime('%B'))
    return render(request, "detailReport.html", {
        "soil": soil["type"],
        "ph": soil["ph"],
        "district": district,
        "sowing": sowing,
        "harvesting": harvesting,
        "month": four_months.strftime('%B'),
        "locust": locust,
        "weathers": weather_response.json,
    })  

def Homepage(request):    
    return render(request, "homepage.html")    

def chat(request):
    posts = requests.get("http://127.0.0.1:8080/dbapi/postmessage")
    replys = requests.get("http://127.0.0.1:8080/dbapi/replymessage")
    if request.method == "POST":
        message = request.POST.get('comment')
        reply = request.POST.get('reply')
        postid = request.POST.get('parentSno')
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
            "PostMessage": postid,
            "reply": reply,   
            "date": date.now         
        }
        requests.post("http://127.0.0.1:8080/dbapi/postmessage", data=value1) 
        requests.post("http://127.0.0.1:8080/dbapi/replymessage", data=value2)      
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

# def login(request):
#     return render(request, "login.html")

def report(request, sowing, harvesting, locust, district):
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
    if locust == '[true]':
        lct = True
    else:
        lct = False
    print(harvest)
    return render(request, "report.html", {
            "sowing": sow,
            "harvesting": harvest,
            "year": date.year,
            "month": date.month,
            "locust": lct,
            "district": district
        })   

# def signup(request):
#     return render(request, "signup.html")

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

# def translate(request):
    

#     driver = webdriver.Firefox()
#     driver.get("http://127.0.0.1:8000/daasapp/Homepage")

#     html = driver.page_source   

#     url = "https://microsoft-translator-text.p.rapidapi.com/translate"

#     querystring = {"to[0]":"am","api-version":"3.0","profanityAction":"NoAction","textType":"plain"}

#     payload = [{"Text": html}]
#     headers = {
#         "content-type": "application/json",
#         "X-RapidAPI-Key": "269f62f524msh775ebacecb3deb0p14e9e2jsn71201fd0fd95",
#         "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
#     }

#     response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

#     print(response.text)

def register(request,*args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home:home")
    context={}
    # if request.method == "GET":

    if request.POST:
        form = UserRegister(request.POST)
        
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user1 = authenticate(email = email, password = raw_password)
            login(request, user1)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("Homepage")
            # passwordConf = request.POST['passwordConf']
            # user = DAAS_User( first_name=first_name, last_name=last_name, phone_number = phone_number, email=email,  password = password)
            # user.save()
            # return redirect("home:home")
        else:
            context["register_form"]=form
            
    else:
        form = UserRegister()
        context['register_form'] = form
    return render(request, "signup.html", context)

    # signin

def signin(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("Homepage")
    
    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))


    if request.POST:
        form = UserLogin(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                # return render(request, "html/logout.html",context)
                return redirect("Homepage")
    else: 
        form = UserLogin()

    context["login_form"]=form
    return render(request, "login2.html", context)   
        # return render(request, "html/signin.html")

def signout(request):
    logout(request)
    # return render(request, "html/signin.html")
    return redirect("Homepage")


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

def view_profile(request):
    return render(request, "html/user_profile.html")