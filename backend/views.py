from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import requests


def link(request):
    method = request.is_secure() and "https" or "http"
    alamat = method+"://" + request.META['HTTP_HOST'];
    return alamat


@login_required
def dashboard(request):
    # equipment = Equipment.objects.get(pk=1)
    # return render(request, 'trend.html', {"equipment":equipment})
    return render(request, 'index.html')


@login_required
def index(request):
    return render(request,'maps.html')


@login_required
def asset_wellness_unit(request,unit):
    response = requests.get(link(request) + '/back/getAW/'+unit)
    unit_data = response.json()
    title = "Asset Wellness " + unit_data["name"]
    reports = unit_data["data"]
    return render(request, 'unit_aw.html',
                  { "title": title,
                   "reports": reports})


@login_required
def asset_wellness_all(request):
    response = requests.get(link(request) + '/back/getAW/')
    condition_data = response.json()
    title = "Asset Wellness"
    units = condition_data["units"]
    return render(request, 'aw.html', {"condition_id": 12, "title": title, "units": units})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def dcs_realtime(request):
    alat = AlatDCS.objects.all()
    unit = Unit.objects.exclude(name="Common")
    return render(request, 'dcs.html',{"alats" : alat,"units":unit})


@login_required
def condition(request,id):
    response = requests.post(link(request)+'/back/condition/',data={"id":id})
    condition_data = response.json()
    id = condition_data["id"]
    title = condition_data["name"]
    units = condition_data["units"]
    return render(request,'condition.html',{"condition_id":id,"title":title,"units":units})


@login_required
def unit(request,kondisi_id,unit_id):
    response = requests.post(link(request)+'/back/unit/',data={"unit_id":unit_id,"kondisi_id":kondisi_id})
    unit_data = response.json()
    title = Condition.objects.get(pk=kondisi_id).name + " " +unit_data["name"]
    reports = unit_data["report"]
    return render(request,'unit.html',{"link":"/back/download/?id_kondisi=%i&id_unit=%i"% (kondisi_id,unit_id),"title":title,"reports":reports})


@login_required
def trend(request,id):
    response = requests.post(link(request)+'/back/trend/',data={"id":id})
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