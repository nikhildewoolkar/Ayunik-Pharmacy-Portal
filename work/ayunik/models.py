from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import *
from django.db.models.signals import post_save
class SignUp(models.Model):
    username=models.CharField(max_length=100)
    utype=models.CharField(max_length=100)
class ClientSignUp(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phoneno=models.CharField(max_length=100)
    address=models.CharField(max_length=250)
    psw=models.CharField(max_length=150)
    utype=models.CharField(max_length=150)
class PharmacySignUp(models.Model):
    pname = models.CharField(max_length=100)
    oname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=100)
    adhar = models.CharField(max_length=100)
    psw=models.CharField(max_length=150)
    utype=models.CharField(max_length=150)
class CUserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    usernames=models.CharField(max_length=50)
    phoneno=models.CharField(max_length=100)
    address=models.CharField(max_length=250)
    utype=models.CharField(max_length=150)
    def __str__(self):  # __str__
        return (self.user.username)

class PUserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    usernames=models.CharField(max_length=100)
    phoneno = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    pan = models.CharField(max_length=100)
    adhar = models.CharField(max_length=100)
    utype=models.CharField(max_length=150)
    def __str__(self):  # __str__
        return (self.user.username)

class Feedback(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    emailadd=models.EmailField(max_length=254)
    subject=models.CharField(max_length=200)
    message=models.CharField(max_length=500)

class Query(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    subject=models.CharField(max_length=200)
    message=models.CharField(max_length=500)

class MedInfo(models.Model):
    medname= models.CharField(max_length=255)
    puname= models.CharField(max_length=255)
    pname= models.CharField(max_length=255)
    add= models.CharField(max_length=255)
    sup= models.CharField(max_length=255)
    medquantity= models.IntegerField()
    medprice= models.IntegerField()
class MedTrack(models.Model):
    medname= models.CharField(max_length=255)
    puname= models.CharField(max_length=255)
    pname= models.CharField(max_length=255)
    add= models.CharField(max_length=255)
    sup= models.CharField(max_length=255)
    medquantity= models.IntegerField()
    medprice= models.IntegerField()
    date= models.CharField(max_length=255)
    expdate= models.CharField(max_length=255)
    reqtype= models.CharField(max_length=255)

class Advertisements(models.Model):
    pname = models.CharField(max_length=255)
    puname= models.CharField(max_length=255)
    padd= models.CharField(max_length=255)
    header = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    startdate = models.CharField(max_length=255)
    enddate = models.CharField(max_length=255)
    createdate = models.CharField(max_length=255)

class TrackAdv(models.Model):
    pname = models.CharField(max_length=255)
    puname= models.CharField(max_length=255)
    padd= models.CharField(max_length=255)
    header = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    startdate = models.CharField(max_length=255)
    enddate = models.CharField(max_length=255)
    createdate = models.CharField(max_length=255)
    action = models.CharField(max_length=255)

class CartData(models.Model):
    cname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    pname = models.CharField(max_length=255)
    puname = models.CharField(max_length=255)
    padd = models.CharField(max_length=255)
    medicineprice = models.IntegerField()
    quantity = models.IntegerField()

class Transaction(models.Model):
    pname=models.CharField(max_length=100)
    puname=models.CharField(max_length=100)
    padd=models.CharField(max_length=100)
    cname=models.EmailField(max_length=254)
    mname=models.CharField(max_length=200)
    price=models.IntegerField()
    quantity=models.IntegerField()
    datetime=models.CharField(max_length=100)

# class Transclient(models.Model):
#     cname=models.CharField(max_length=100)
#     pname=models.CharField(max_length=100)
#     puname=models.CharField(max_length=100)
#     padd=models.CharField(max_length=100)
#     mname=models.EmailField(max_length=254)
#     price=models.IntegerField()
#     quantity=models.IntegerField()
#     datetime=models.CharField(max_length=100)
# class Transpharmacy(models.Model):
#     cname=models.CharField(max_length=100)
#     pname=models.CharField(max_length=100)
#     puname=models.CharField(max_length=100)
#     padd=models.CharField(max_length=100)
#     mname=models.EmailField(max_length=254)
#     price=models.IntegerField()
#     quantity=models.IntegerField()
#     datetime=models.CharField(max_length=100)