from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import random
import string
from django.core.mail import EmailMultiAlternatives
from charities.settings import EMAIL_HOST_USER
# Create your views here.

def index(request):
    active = False
    cities = City.objects.all()
    frstID = cities[0].id
    spess = Speciality.objects.all()
    frstIDSp = spess[0].id
    if request.user.is_authenticated:
        charities = Charity.objects.filter(userID=str(request.user.id))
        charitiesCount = 0
        for ch in charities:
            charitiesCount += 1
        if charitiesCount < int(request.user.userMaxPages):
            active = True
    return render(request, "charity/index.html", {
        "active":active,
        "super":request.user.is_superuser,
        "cities": cities,
        "frstID": frstID,
        "spess": spess,
        "frstIDSp": frstIDSp
    })

def results(request):
    cities = City.objects.all()
    frstID = cities[0].id
    spess = Speciality.objects.all()
    frstIDSp = spess[0].id
    active = False
    if request.user.is_authenticated:
        charities = Charity.objects.filter(userID=str(request.user.id))
        charitiesCount = 0
        for ch in charities:
            charitiesCount += 1
        if charitiesCount < int(request.user.userMaxPages):
            active = True
    if request.method == "POST":
        charitiesList = Charity.objects.all()
        cityID = request.POST["cityID"]
        city = City.objects.get(id=cityID)
        specialityID = request.POST["specialityID"]
        speciality = Speciality.objects.get(id=specialityID)
        order = request.POST["order"]
        search = request.POST["search"]
        charities = []
        if search:
            for charity in charitiesList:
                if search == charity.name or search == charity.googleMapLink or search == charity.address or search == charity.telephoneNumber or search == charity.anotherPhoneNumber or search == charity.phoneNumber or search == charity.youtube or search == charity.twitter or search == charity.facebook or search == charity.storeLink or search == charity.webLink:

                    if charity.activeState == True:
                        return render(request, "charity/charity page.html", {
                            "charity":charity
                        })
                elif search in charity.name or search in charity.googleMapLink or search in charity.address or search in charity.telephoneNumber or search in charity.anotherPhoneNumber or search in charity.phoneNumber or search in charity.youtube or search in charity.twitter or search in charity.facebook or search in charity.storeLink or search in charity.webLink:
                    if charity.city.id == city.id:
                        if charity.speciality.id == speciality.id:
                            if charity.activeState == True:
                                charities.append(charity)
                        else:
                            if charity.activeState == True:
                                charities.append(charity)
                    elif charity.speciality.id == speciality.id:
                        if charity.activeState == True:
                            charities.append(charity)
                    else:
                        if charity.activeState == True:
                            charities.append(charity)
                else:
                    if charity.city.id == city.id:
                        if charity.speciality.id == speciality.id:
                            if charity.activeState == True:
                               charities.append(charity)
                        else:
                            if charity.activeState == True:
                                charities.append(charity)
                    else:
                        if charity.speciality.id == speciality.id:
                            if charity.activeState == True:
                                charities.append(charity)
        else:
            for charity in charitiesList:
                if charity.city.id == city.id:
                    if charity.speciality.id == speciality.id:
                        if charity.activeState == True:
                            charities.append(charity)
                    else:
                        if charity.activeState == True:
                            charities.append(charity)
                else:
                    if charity.speciality.id == speciality.id:
                        if charity.activeState == True:
                            charities.append(charity)

        if charities:
            if order == "2":
                charities.sort(key=lambda x: x.id, reverse=True)
        else:
            return render(request, "charity/results.html", {
                "charities": charities,
                "active":active,
                "message":"لا يوجد جمعية بهذه المواصفات",
                "super": request.user.is_superuser,
                "cities": cities,
                "frstID": frstID,
                "spess": spess,
                "frstIDSp": frstIDSp
            })
        paginator = Paginator(charities, 3)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            charities1 = paginator.page(page)
        except(EmptyPage, InvalidPage):
            charities1 = paginator.page(paginator.num_pages)
        return render(request, "charity/results.html", {
            "charities":charities1,
            "active":active,
            "super": request.user.is_superuser,
            "cities": cities,
            "frstID": frstID,
            "spess": spess,
            "frstIDSp": frstIDSp
        })
    elif request.method == "GET":
        charities = Charity.objects.all()
        paginator = Paginator(charities, 3)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            charities1 = paginator.page(page)
        except(EmptyPage, InvalidPage):
            charities1 = paginator.page(paginator.num_pages)
        return render(request, "charity/results.html", {
            "charities": charities1,
            "active":active,
            "super": request.user.is_superuser,
            "cities": cities,
            "frstID": frstID,
            "spess": spess,
            "frstIDSp": frstIDSp
        })
def charityPage(request, name):
    charity = Charity.objects.get(name=name)
    if charity.activeState:
        owner = False
        if request.user.id == int(charity.userID):
            owner = True
        return render(request, "charity/charity page.html", {
            "charity":charity,
            "owner":owner
        })
    else:
        return render(request, "charity/not activated.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "charity/login.html", {
                "message": "خطأ في اسم المستخدم او كلمة المرور"
            })
    else:
        return render(request, "charity/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request, accessCode):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "charity/register.html", {
                "message": "يجب أن يكون تأكيد كلمة المرور ككلمة المرور نفسها",
                "string":accessCode
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "charity/register.html", {
                "message": "اسم المستخدم تم استخدامه من قبل",
                "string":accessCode
            })
        login(request, user)
        OneTimeLinkModel.objects.filter(oneTimeCode=accessCode).delete()

        return HttpResponseRedirect(reverse("index"))
    else:
        if OneTimeLinkModel.objects.filter(oneTimeCode=accessCode).exists():
            return render(request, "charity/register.html", {
                "string":accessCode
            })
        else:
            return render(request, "charity/expired link.html")

def createPage(request):
    charities = Charity.objects.all()
    cities = City.objects.all()
    frstID = cities[0].id
    spess = Speciality.objects.all()
    frstIDSp = spess[0].id
    if request.method == "GET":
        if request.user.is_authenticated:
            userMaxPages = request.user.userMaxPages
            createdCharities = Charity.objects.filter(userID=request.user.id).all()
            createdCharitiesCount = 0
            for charity in createdCharities:
                createdCharitiesCount += 1
            if createdCharitiesCount < userMaxPages:
                return render(request, "charity/create.html", {
                    "cities":cities,
                    "frstID":frstID,
                    "spess":spess,
                    "frstIDSp":frstIDSp
                })
            else:
                return render(request, "charity/unavailable.html")
        else:
            return render(request, "charity/unavailable.html")
    elif request.method == "POST":
        userID = request.user.id
        name = request.POST["name"]
        c = False
        for ch in charities:
            if ch.name == name:
                c = True
        if c:
            return render(request, "charity/create.html", {
                "message":"هذا الاسم موجود من قبل",
                "cities":cities,
                "frstID":frstID,
                "spess": spess,
                "frstIDSp": frstIDSp
            })
        else:
            webLink = request.POST["webLink"]
            storeLink = request.POST["storeLink"]
            cityID = request.POST["cityID"]
            city = City.objects.get(id=cityID)
            specialityID = request.POST["specialityID"]
            speciality = Speciality.objects.get(id=specialityID)
            facebook = request.POST["facebook"]
            twitter = request.POST["twitter"]
            youtube = request.POST["youtube"]
            phoneNumber = request.POST["phoneNumber"]
            anotherPhoneNumber = request.POST["anotherPhoneNumber"]
            telephoneNumber = request.POST["telephoneNumber"]
            address = request.POST["address"]
            googleMapLink = request.POST["googleMapLink"]
            activeState = False
            charity = Charity(userID=userID, name=name, webLink=webLink, storeLink=storeLink,
                              city=city, speciality=speciality, facebook=facebook, twitter=twitter,
                              youtube=youtube, phoneNumber=phoneNumber, anotherPhoneNumber=anotherPhoneNumber,
                              telephoneNumber=telephoneNumber, address=address, googleMapLink=googleMapLink, activeState=activeState)
            if len(request.FILES) != 0:
                charity.slogan = request.FILES['slogan']
            charity.save()
            return redirect("charityPage", name=charity.name)

def edit(request, name):
    charity = Charity.objects.get(name=name)
    if request.method == "GET":
        mekka = False
        madina = False
        riyad = False
        qu = False
        ay = False
        mo = False
        if charity.city.id == 1:

            mekka = True
        elif charity.city.id == 2:
            madina = True
        else:
            riyad = True
        if charity.speciality.id == 1:
            qu = True
        elif charity.speciality.id == 2:
            ay = True
        else:
            mo = True

        return render(request, "charity/edit.html", {
            "charity":charity, "mekka":mekka, "madina":madina, "riyad":riyad, "qu":qu, "ay":ay, "mo":mo
        })
    elif request.method == "POST":
        userID = request.user.id
        name = request.POST["name"]

        webLink = request.POST["webLink"]
        storeLink = request.POST["storeLink"]
        cityID = request.POST["cityID"]
        city = City.objects.get(id=cityID)
        specialityID = request.POST["specialityID"]
        speciality = Speciality.objects.get(id=specialityID)
        facebook = request.POST["facebook"]
        twitter = request.POST["twitter"]
        youtube = request.POST["youtube"]
        phoneNumber = request.POST["phoneNumber"]
        anotherPhoneNumber = request.POST["anotherPhoneNumber"]
        telephoneNumber = request.POST["telephoneNumber"]
        address = request.POST["address"]
        googleMapLink = request.POST["googleMapLink"]
        charity.city = city
        charity.speciality = speciality
        charity.webLink = webLink
        charity.storeLink = storeLink
        charity.facebook = facebook
        charity.twitter = twitter
        charity.youtube = youtube
        charity.phoneNumber = phoneNumber
        charity.anotherPhoneNumber = anotherPhoneNumber
        charity.telephoneNumber = telephoneNumber
        charity.address = address
        charity.googleMapLink = googleMapLink
        charity.name = name
        if len(request.FILES) != 0:
            charity.slogan = request.FILES['slogan']
        charity.save()
        return redirect("charityPage", name=charity.name)

def sendEmails(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, "charity/send emails.html")
            else:
                return render(request, "charity/unavailable.html")
        else:
            return render(request, "charity/unavailable.html")
    elif request.method == "POST":
        recivingMailsStr = request.POST["toEmail"]
        recivingMailsList = recivingMailsStr.split(", ")
        for mail in recivingMailsList:
            letters = string.ascii_lowercase
            theString = ''.join(random.choice(letters) for i in range(8))
            OneTimeLinkModel.objects.create(oneTimeCode=theString)
            link = f"127.0.0.1:8000/register/{theString}"
            msg = EmailMultiAlternatives('سجل معنا في موقع دليل الجمعيات الخيرية', f" {link}رابط التسجيل  ", EMAIL_HOST_USER, [f'{mail}'])
            msg.send()
        return HttpResponseRedirect(reverse('index'))

