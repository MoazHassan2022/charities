from django.contrib.auth.models import AbstractUser
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=64, default="", blank=True)
    def __str__(self):
        return f"{self.name}"
class Speciality(models.Model):
    name = models.CharField(max_length=64, default="", blank=True)
    def __str__(self):
        return f"{self.name}"
class Charity(models.Model):
    userID = models.CharField(max_length=64, default="", blank=True)
    name = models.CharField(max_length=64, default="", blank=True)
    slogan = models.ImageField(blank=True, null=True)
    webLink = models.CharField(max_length=150, default="", blank=True)
    storeLink = models.CharField(max_length=150, default="", blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=150, default="", blank=True)
    twitter = models.CharField(max_length=150, default="", blank=True)
    youtube = models.CharField(max_length=150, default="", blank=True)
    phoneNumber = models.CharField(max_length=64, default="", blank=True)
    anotherPhoneNumber = models.CharField(max_length=150, default="", blank=True)
    telephoneNumber = models.CharField(max_length=150, default="", blank=True)
    address = models.CharField(max_length=150, default="", blank=True)
    googleMapLink = models.CharField(max_length=150, default="", blank=True)
    activeState = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return f"{self.name} : status : {self.activeState}"
class User(AbstractUser):
    charityList = models.ManyToManyField(Charity, blank=True, related_name="charityUsers")
    userMaxPages = models.IntegerField(default=1, blank=True)

class OneTimeLinkModel(models.Model):
    oneTimeCode = models.CharField(max_length=10)