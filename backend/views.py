from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import requests

# TODO : BUAT HALAMAN TREND , FLOTCHARTS DYNAMIC


def test(request):
    equipment = Equipment.objects.get(pk=1)
    return render(request, 'trend.html', {"equipment":equipment})


@login_required
def index(request):
    return render(request,'index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def condition(request,id):
    response = requests.post('http://'+request.META['HTTP_HOST']+'/back/condition/',data={"id":id})
    condition_data = response.json()
    id = condition_data["id"]
    title = condition_data["name"]
    units = condition_data["units"]
    return render(request,'condition.html',{"condition_id":id,"title":title,"units":units})


@login_required
def unit(request,kondisi_id,unit_id):
    response = requests.post('http://'+request.META['HTTP_HOST']+'/back/unit/',data={"unit_id":unit_id,"kondisi_id":kondisi_id})
    unit_data = response.json()
    title = Condition.objects.get(pk=kondisi_id).name + " " +unit_data["name"]
    reports = unit_data["report"]
    return render(request,'unit.html',{"title":title,"reports":reports})


@login_required
def trend(request,id):
    response = requests.post('http://'+request.META['HTTP_HOST']+'/back/trend/',data={"id":id})
    eqt = Equipment.objects.get(pk=id)
    eqt_data = response.json()
    title = eqt.Condition.name + " | " + eqt.Unit.name
    datas = eqt_data["data"]
    return render(request,'trend.html',{"equipment":eqt,"title":title,"datas":datas})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})