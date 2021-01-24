from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
import datetime
import os
from django.conf import settings
from django.core.mail import send_mail 
import numpy as np
from django.contrib import messages
from subprocess import check_output, CalledProcessError,STDOUT
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, request
from .models import CUserProfile,ClientSignUp,PUserProfile,PharmacySignUp,Feedback,SignUp,Query,Advertisements
from .models import MedInfo,MedTrack,TrackAdv,CartData,Transaction
# Create your views here.
def home(request):
    return render(request,"home.html")
def about(request):
    return render(request,"about.html")
def phome(request):
    p1=request.user
    if(p1.username==""):
        return render(request,"phome.html")
    else:    
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        return render(request,"phome.html",{"j":j})
def pabout(request):
    p1=request.user
    if(p1.username==""):
        return render(request,"pabout.html")
    else:    
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        return render(request,"pabout.html",{"j":j})
def contact(request):
    return render(request,"contact.html")
def adv(request):
    x = PharmacySignUp.objects.all()
    if request.method=="POST":
        id=request.POST.get("id")
        n = Advertisements.objects.filter(puname=id)
        if(Advertisements.objects.filter(puname=id).count()==0):
            msg="No Advertisement Available"                                    
        else:
            msg=""
        return render(request,"adv.html",{'n':n,'x':x,"msg":msg})
    n = Advertisements.objects.all()
    return render(request,"adv.html",{"n":n,"x":x})
def signup(request):
    return render(request,"signup.html")
def login(request):
    return render(request,"login.html")
def store(request):
    x = PharmacySignUp.objects.all()
    v=MedInfo.objects.all()
    return render(request,"store.html",{'v':v,'x':x})
def cart(request):
    p1=request.user
    cname=p1.username
    v=CartData.objects.filter(cname=cname)
    j=CartData.objects.filter(cname=cname)
    print(v.count())
    total=0
    for j in j:
        total+=(j.medicineprice*j.quantity)
    return render(request,"cart.html",{'v':v,"total":total})
def cartdel(request):
    x = PharmacySignUp.objects.all()
    v=MedInfo.objects.all()
    p1=request.user
    cname=p1.username
    v=CartData.objects.filter(cname=cname)
    j=CartData.objects.filter(cname=cname)
    total=0
    for j in j:
        total+=(j.medicineprice*j.quantity)
    if request.method=="POST":
        if 'delete' in request.POST:    
            mname=request.POST.get("mname")
            pname=request.POST.get("pname")
            padd=request.POST.get("padd")
            cname=p1.username
            k=CartData.objects.filter(cname=cname,mname=mname,pname=pname,padd=padd).delete()
            v=CartData.objects.filter(cname=cname)
            j=CartData.objects.filter(cname=cname)
            total=0
            for j in j:
                total+=(j.medicineprice*j.quantity)
            return render(request,"cart.html",{'v':v,"total":total})
        if 'update' in request.POST:
            p1==request.user
            mname=request.POST.get("mname")
            pname=request.POST.get("pname")
            padd=request.POST.get("padd")
            cname=p1.username
            quantity=int(request.POST.get("quantity"))
            CartData.objects.filter(cname=cname,mname=mname,pname=pname,padd=padd).update(quantity=quantity)
            v=CartData.objects.filter(cname=cname)
            j=CartData.objects.filter(cname=cname)
            total=0
            for j in j:
                total+=(j.medicineprice*j.quantity)
            return render(request,"cart.html",{'v':v,"total":total})
    return render(request,"cart.html",{'v':v,"total":total})
def cartadd(request):
    x = PharmacySignUp.objects.all()
    v=MedInfo.objects.all()
    p1=request.user
    if request.method=="POST":
        medname=request.POST.get("mname")
        pname=request.POST.get("pname")
        padd=request.POST.get("padd")
        price=int(request.POST.get("price"))
        quantity=1
        cname=p1.username
        c=MedInfo.objects.get(medname=medname,pname=pname)
        puname=c.puname
        print(medname,pname,padd,price,quantity,puname,cname)
        f=CartData(mname=medname,pname=pname,padd=padd,medicineprice=price,quantity=quantity,puname=puname,cname=cname)
        f.save()
        return render(request,"store.html",{'v':v,'x':x})
    return render(request,"store.html",{'v':v,'x':x})

def checkout(request):
    if request.method=="POST":     
        g=int(request.POST.get("id"))
        return render(request,"checkout.html",{"g":g})
    return render(request,"checkout.html")

def order(request):
    p1=request.user
    cname=p1.username
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        uname=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        add=request.POST.get("add")
        psw=request.POST.get("pass")
        x = datetime.datetime.now()
        g=1
        u1 = ClientSignUp.objects.get(username=uname)
        if (u1.psw!=psw):
            messages.info(request,'password is not valid')
            print(1,2,2)
            return render(request,"checkout.html",{"g":g})
        else:
            k=[]
            b=CartData.objects.filter(cname=cname)
            for i in b:
                if(i.puname not in k):
                    k.append(i.puname)
                Transaction(puname=i.puname,pname=i.pname,padd=i.padd,cname=i.cname,mname=i.mname,price=i.medicineprice,quantity=i.quantity, datetime=x).save()
                MedTrack(medname=i.mname,puname=i.puname,pname=i.pname,add=i.padd,sup=i.cname,medquantity=i.quantity,medprice=i.medicineprice,date=x,expdate="00-00-0000",reqtype="OrderPlacedUpdate").save()
                xin=MedInfo.objects.get(puname=i.puname,medname=i.mname)
                qua=int(xin.medquantity)-int(i.quantity)
                MedInfo.objects.filter(puname=i.puname,medname=i.mname).update(medquantity=qua)
            subject = 'Order Successfully Placed'
            message = f'Hi {p1.username}, thank you for Ordering medicines.we will deliver the order within 30 mins.'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [p1.email] 
            send_mail( subject, message, email_from, recipient_list ,fail_silently=False) 
            h=[]
            for i in range(len(k)):
                j=PharmacySignUp.objects.get(username=k[i])
                h.append(j.email)
            subject = 'Order Successfully Placed'
            message = f'Hi ,{fname} {lname} ({uname}), phone No.:-{phone},Email:-{email},Address:-{add} have ordered medicines from your pharmacy.kindly check client order details from tou transaction track manage portal and deliver the order within 30 mins.thank you.'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = h 
            print(recipient_list)
            send_mail( subject, message, email_from, recipient_list,fail_silently=False ) 
            b=CartData.objects.filter(cname=cname)
            b.delete()
            messages.info(request,'Order Placed')
            return render(request,"checkout.html",{"g":g})
    return render(request,"checkout.html")

def storesearch(request):
    if request.method=="POST":     
        medname=request.POST.get("id")
        x = PharmacySignUp.objects.all()
        print(medname)
        v=MedInfo.objects.filter(puname=medname)
        # v=MedInfo.objects.filter(medname=medname)
        return render(request,"store.html",{'v':v,'x':x})
    v=MedInfo.objects.all()
    return render(request,"store.html",{'v':v})

def storesearchs(request):
    if request.method=="POST":     
        medname=request.POST.get("mname")
        x = PharmacySignUp.objects.all()
        print(medname)
        v=MedInfo.objects.filter(medname=medname)
        return render(request,"store.html",{'v':v,'x':x})
    v=MedInfo.objects.all()
    return render(request,"store.html",{'v':v})

def profile(request):
    p1=request.user
    id=""
    n=Transaction.objects.filter(cname=p1.username)
    if request.method=="POST":
        id=int(request.POST.get("id"))
        return render(request,"profile.html",{"id":id,'n':n})
    return render(request,"profile.html",{"id":id,'n':n})
def pharmacysignup(request):
    if request.method=='POST':
        first_name=request.POST.get("pname")
        last_name=request.POST.get("oname")
        username = request.POST.get("uid")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        add= request.POST.get("add")
        pan= request.POST.get("pan")
        adhar= request.POST.get("adhar")
        password=request.POST.get("pass")
        password1=request.POST.get("pass1")
        utype="p"
        print(username)
        def password_check(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 8') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            if val == False: 
                val=True
                return val
                print(val)
        if (password_check(password)): 
            print("y")
        else: 
            print("x")
        #print(password)                    
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('pharmacysignup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('pharmacysignup')
            elif (password_check(password)):
                messages.info(request,'password is not valid')
                print("harshad")
                return redirect('pharmacysignup')
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                user.save()
                work1=PharmacySignUp(pname=first_name,oname=last_name,username=username,phoneno=phoneno,email=email,address=add,pan=pan,adhar=adhar,psw=password,utype=utype)
                work1.save()
                work2=SignUp(username=username,utype=utype)
                work2.save()
                messages.info(request,"user created succesfully")
                user=auth.authenticate(username=username,password=password)
                if user is not None:
                   auth.login(request,user)
                print("nikhil")
                u = User.objects.get(username=username)
                reg=PUserProfile(user=u,usernames=username,phoneno=phoneno,address=add,utype=utype,pan=pan,adhar=adhar)
                reg.save()
                print("dewoolkar")
                auth.logout(request)
                print("nitin")
        else:
            messages.info(request,"password not matching")
            return redirect('pharmacysignup')
        return redirect('pharmacylogin')
    return render(request,"pharmacysignup.html")

    return render(request,"pharmacysignup.html")
def pharmacylogin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        utype="p"
        print(username)
        print(password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            p1=request.user
            return redirect('/padmin')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('pharmacylogin')
    return render(request,"pharmacylogin.html")
def clientsignup(request):
    if request.method=='POST':
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        username = request.POST.get("uid")
        phoneno=request.POST.get("phoneno")
        add= request.POST.get("add")
        email=request.POST.get("email")
        password=request.POST.get("pass")
        password1=request.POST.get("pass1")
        utype="c"
        def password_check(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 8') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            if val == False: 
                val=True
                return val
                print(val)
        if (password_check(password)): 
            print("y")
        else: 
            print("x")
        #print(password)                    
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('clientsignup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('clientsignup')
            elif (password_check(password)):
                messages.info(request,'password is not valid')
                return redirect('clientsignup')
            else:
                user=User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                user.save()
                work=ClientSignUp(username=username,psw=password,email=email,first_name=first_name,last_name=last_name,phoneno=phoneno,address=add,utype=utype)
                work.save()
                work1=SignUp(username=username,utype=utype)
                work1.save()
                messages.info(request,"user created succesfully")
                user=auth.authenticate(username=username,password=password)
                if user is not None:
                   auth.login(request,user)
                print("nikhil")
                u = User.objects.get(username=username)
                reg=CUserProfile(user=u,usernames=username,phoneno=phoneno,address=add,utype=utype)
                reg.save()
                print("dewoolkar")
                auth.logout(request)
                print("nitin")
        else:
            messages.info(request,"password not matching")
            return redirect('clientsignup')
        return redirect('clientlogin')
    return render(request,"clientsignup.html")

def clientlogin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("pwd")
        print(username)
        print(password)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            p=request.user
            print(p.password)
            return redirect('/')#,{'pics':pics,"id":id,'pdf':pdf,'vlink':vlink}
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('clientlogin')
    return render(request,"clientlogin.html")

def logout(request):
    auth.logout(request)
    return render(request,"home.html")

def ceditprofile(request):
    p=request.user
    if request.method=="POST":
        id=2
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        uname=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        add=request.POST.get("add")
        pass1=request.POST.get("pass")
        u1 = ClientSignUp.objects.get(username=p.username)
        if (u1.psw!=pass1):
            messages.info(request,'password is not valid')
            return render(request,"profile.html",{"id":id})
        else:    
            User.objects.filter(username=uname).update(first_name=fname,last_name=lname)
            CUserProfile.objects.filter(usernames=uname).update(phoneno=phone,address=add)
            ClientSignUp.objects.filter(username=uname).update(first_name=fname,last_name=lname,phoneno=phone,address=add)
            return render(request,"profile.html",{"id":id})
    id=2
    return render(request,"pprofile.html",{"id":id})
def peditprofile(request):
    p=request.user
    if request.method=="POST":
        j="p"
        id=2
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        uname=request.POST.get("username")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        add=request.POST.get("add")
        pan=request.POST.get("pan")
        adhar=request.POST.get("adhar")
        pass1=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p.username)
        if (u1.psw!=pass1):
            messages.info(request,'password is not valid')
            return render(request,"pprofile.html",{"id":id,"j":j})
        else:    
            User.objects.filter(username=uname).update(first_name=fname,last_name=lname)
            PUserProfile.objects.filter(usernames=uname).update(phoneno=phone,address=add)
            PharmacySignUp.objects.filter(username=uname).update(pname=fname,oname=lname,phoneno=phone,address=add,pan=pan,adhar=adhar)
            return render(request,"pprofile.html",{"id":id,"j":j})
    p1=request.user
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    id=2
    return render(request,"pprofile.html",{"id":id,"j":j})

def fb(request):
    if request.method=="POST":
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        sub=request.POST.get("sub")
        msg=request.POST.get("msg")
        register=Feedback(firstname=fname ,lastname=lname,emailadd=email ,subject=sub ,message=msg)
        register.save()
    return render(request,"contact.html")
def padmin(request):
    p1=request.user
    if(p1.username==""):
        return render(request,"padmin.html")
    else:    
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        return render(request,"padmin.html",{"j":j})
        
def pprofile(request):
    p1=request.user
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        id=int(request.POST.get("id"))
        return render(request,"pprofile.html",{"id":id,"j":j})
    else:
        id=0
        if(p1.username==""):
            return render(request,"pprofile.html")
        else:
            u = SignUp.objects.get(username=p1.username)
            j=u.utype
            return render(request,"pprofile.html",{"j":j})


def query(request):
    p1=request.user
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        username=request.POST.get("uname")
        email=request.POST.get("email")
        subject=request.POST.get("sub")
        message=request.POST.get("msg")
        data=Query(username=username,email=email,subject=subject,message=message)
        data.save()
        q="Query succesfully sent.."
        return render(request,"query.html",{"j":j,"q":q})
    if(p1.username==""):
        return render(request,"query.html")
    else:    
        q=""
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        return render(request,"query.html",{"j":j,"q":q})

def cchange_password(request):
    if request.method == 'POST':
        old=request.POST.get("old")
        new1=request.POST.get("new1")
        new2=request.POST.get("new2")
        def passwordcheck(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 20') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            return val
        p=request.user
        u1 = ClientSignUp.objects.get(username=p.username)
        if(u1.psw==old):
            print(u1.psw,old)
            if(new1==new2):
                password=new1
                print(new1,new2)
                print(passwordcheck(password))
                if(passwordcheck(password)==True):
                    u = User.objects.get(username=p.username)
                    u.set_password(new1)
                    u.save()
                    ClientSignUp.objects.filter(username=p.username).update(psw=new1)
                    messages.info(request,"password Changed succesfully")
                    return redirect('/cchange_password')
        else:
            messages.info(request,"Error Occured")
            id=3
            return render(request,"pprofile.html",{"id":id})
    id=3
    return render(request,"pprofile.html",{"id":id})

def pchange_password(request):
    if request.method == 'POST':
        old=request.POST.get("old")
        new1=request.POST.get("new1")
        new2=request.POST.get("new2")
        def passwordcheck(password):
            SpecialSym =['$', '@', '#', '%'] 
            val = True
            if len(password) < 8:
                print('length should be at least 6') 
                val = False
            if len(password) > 20: 
                print('length should be not be greater than 20') 
                val = False
            if not any(char.isdigit() for char in password): 
                print('Password should have at least one numeral') 
                val = False
            if not any(char.isupper() for char in password): 
                print('Password should have at least one uppercase letter') 
                val = False
            if not any(char.islower() for char in password): 
                print('Password should have at least one lowercase letter') 
                val = False
            if not any(char in SpecialSym for char in password): 
                print('Password should have at least one of the symbols $@#') 
                val = False
            return val
        p=request.user
        u1 = PharmacySignUp.objects.get(username=p.username)
        if(u1.psw==old):
            print(u1.psw,old)
            if(new1==new2):
                password=new1
                print(new1,new2)
                print(passwordcheck(password))
                if(passwordcheck(password)==True):
                    u = User.objects.get(username=p.username)
                    u.set_password(new1)
                    u.save()
                    PharmacySignUp.objects.filter(username=p.username).update(psw=new1)
                    messages.info(request,"password Changed succesfully")
                    return redirect('/pchange_password')
        else:
            messages.info(request,"Error Occured")
            j="p"
            id=3
            return render(request,"pprofile.html",{"id":id,"j":j})
    p1=request.user
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    id=3
    return render(request,"pprofile.html",{"id":id,"j":j})

def psell(request):
    p1=request.user
    x = datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        n = Advertisements.objects.filter(puname=p1.username)
        id=int(request.POST.get("id"))
        return render(request,"psell.html",{"id":id,"j":j,"now":now,'n':n})
    else:
        id=0
        if(p1.username==""):
            return render(request,"psell.html")
        else:    
            u = SignUp.objects.get(username=p1.username)
            j=u.utype
            return render(request,"psell.html",{"j":j,"now":now})

def createadv(request):
    p1=request.user
    x = datetime.datetime.now()
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    id=1
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        pname=request.POST.get("pname")
        puname=request.POST.get("uname")
        padd=request.POST.get("add")
        header=request.POST.get("head")
        text=request.POST.get("msg")
        startdate=request.POST.get("sdate")
        enddate=request.POST.get("edate")
        createdate=request.POST.get("cdate")
        psw=request.POST.get("pass")
        action="AdvertisementAdded"
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=psw):
            print("nick..")
            messages.info(request,'password is not valid')
            return render(request,"psell.html",{"id":id,"j":j,"now":now})
        else:
            if(Advertisements.objects.filter(puname=puname,header=header).exists()):
                print("nick1")
                messages.info(request,'Header Exists')
                return render(request,"psell.html",{"id":id,"j":j,"now":now})
            else:
                print("nick2")
                t=Advertisements(pname=pname,puname=puname,padd=padd,header=header,text=text,startdate=startdate,enddate=enddate,createdate=createdate)
                t.save()
                t1=TrackAdv(pname=pname,puname=puname,padd=padd,header=header,text=text,startdate=startdate,enddate=enddate,createdate=createdate,action=action)
                t1.save()
                messages.info(request,'Advertisement Added')
                return render(request,"psell.html",{"id":id,"j":j,"now":now})
    return render(request,"psell.html",{"id":id,"j":j,"now":now})

def deleteadv(request):
    p1=request.user
    x = datetime.datetime.now()
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    n = Advertisements.objects.filter(puname=p1.username)
    id=2
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        action="AdvertisementDeleted"
        header=request.POST.get("id")
        psw=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=psw):
            print("nick..")
            messages.info(request,'password is not valid')
            return render(request,"psell.html",{"id":id,"j":j,"now":now,'n':n})
        else:
            g=Advertisements.objects.get(puname=p1.username,header=header)
            t1=TrackAdv(pname=g.pname,puname=g.puname,padd=g.padd,header=g.header,text=g.text,startdate=g.startdate,enddate=g.enddate,createdate=g.createdate,action=action)
            t1.save()
            Advertisements.objects.filter(puname=p1.username,header=header).delete()
            return render(request,"psell.html",{"id":id,"j":j,"now":now,'n':n})   
    return render(request,"psell.html",{"id":id,"j":j,"now":now,'n':n})
        
def psmanage(request):
    p1=request.user
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        id=int(request.POST.get("id"))
        if(id == 1):
            n = MedInfo.objects.filter(puname=p1.username)
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n})
        if(id == 2):
            x = datetime.datetime.now()
            now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            return render(request,"psmanage.html",{"id":id,"j":j,"now":now})
        if(id == 3):
            n=MedInfo.objects.filter(puname=p1.username)
            x = datetime.datetime.now()
            now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            # now1=(x.strftime("%Y")+2)+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            return render(request,"psmanage.html",{"id":id,"j":j,"n":n,"now":now})
        if(id == 4):
            x = datetime.datetime.now()
            now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            # now1=(x.strftime("%Y")+2)+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            n=MedInfo.objects.filter(puname=p1.username)
            return render(request,"psmanage.html",{"id":id,"j":j,"n":n,"now":now})
        if(id == 5):
            x = datetime.datetime.now()
            now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            # now1=(x.strftime("%Y")+2)+"-"+x.strftime("%m")+"-"+x.strftime("%d")
            n=MedInfo.objects.filter(puname=p1.username)
            return render(request,"psmanage.html",{"id":id,"j":j,"n":n,"now":now})
    else:
        id=0
        if(p1.username==""):
            return render(request,"psmanage.html")
        else:
            u = SignUp.objects.get(username=p1.username)
            j=u.utype
            return render(request,"psmanage.html",{"j":j})

def ptmanage(request):
    p1=request.user
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        id=int(request.POST.get("id"))
        if(id == 1):
            n = MedInfo.objects.filter(puname=p1.username)
            return render(request,"ptmanage.html",{"id":id,"j":j,'n':n})
        if(id == 2):
            x = MedTrack.objects.filter(puname=p1.username)
            return render(request,"ptmanage.html",{"id":id,"j":j,'x':x})
        if(id == 3):
            n = TrackAdv.objects.filter(puname=p1.username)
            return render(request,"ptmanage.html",{"id":id,"j":j,'n':n})
        if(id == 4):
            n = Transaction.objects.filter(puname=p1.username)
        return render(request,"ptmanage.html",{"id":id,"j":j,'n':n})
    if(p1.username==""):
        return render(request,"ptmanage.html")
    else:    
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        return render(request,"ptmanage.html",{"j":j})

def addmed(request):
    if request.method=="POST":
        p1=request.user
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        id=2
        x = datetime.datetime.now()
        now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
        mname=request.POST.get("mname")
        uname=request.POST.get("uname")
        pname=request.POST.get("pname")
        address=request.POST.get("add")
        supplier=request.POST.get("sup")
        quantity=int(request.POST.get("quant"))
        price=int(request.POST.get("price"))
        date=request.POST.get("date")
        expdate=request.POST.get("exp")
        reqtype="addmedicine"
        password=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=password):
            print("nick..")
            messages.info(request,'password is not valid')
            return render(request,"psmanage.html",{"id":id,"j":j,"now":now})
        else:
            print("nick")
            if MedInfo.objects.filter(puname=uname,medname=mname).exists():
                print("nick1")
                messages.info(request,'Medicine Exists...please update Medicine data')
                return render(request,"psmanage.html",{"id":id,"j":j,"now":now})
            else:
                print("nick2")
                t=MedInfo(medname=mname,puname=uname,pname=pname,add=address,sup=supplier,medquantity=quantity,medprice=price)
                t.save()
                t1=MedTrack(medname=mname,puname=uname,pname=pname,add=address,sup=supplier,medquantity=quantity,medprice=price,date=date,expdate=expdate,reqtype=reqtype)
                t1.save()
                messages.info(request,'Medicine added')
                return render(request,"psmanage.html",{"id":id,"j":j,"now":now})
    p1=request.user
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    id=2
    return render(request,"psmanage.html",{"id":id,"j":j,"now":now})

def upmed(request):
    p1=request.user
    n=MedInfo.objects.filter(puname=p1.username)
    x = datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    if request.method=="POST":
        u = SignUp.objects.get(username=p1.username)
        j=u.utype
        id=3
        mname=request.POST.get("id")
        uname=request.POST.get("uname")
        pname=request.POST.get("pname")
        address=request.POST.get("add")
        quantity=int(request.POST.get("quant"))
        date=request.POST.get("date")
        expdate=request.POST.get("exp")
        reqtype="updateaddmedicine"
        password=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=password):
            messages.info(request,'password is not valid')
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
        else:
            fin=MedInfo.objects.filter(puname=uname,medname=mname)
            for fin in fin:
                print(fin.medquantity)
            qua=int(quantity)+int(fin.medquantity)
            MedInfo.objects.filter(puname=uname,medname=mname).update(medquantity=qua)
            t1=MedTrack(medname=mname,puname=uname,pname=pname,add=address,sup=fin.sup,medquantity=quantity,medprice=fin.medprice,date=date,expdate=expdate,reqtype=reqtype)
            t1.save()
            messages.info(request,'Medicine quantity increased')
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
    p1=request.user
    u = SignUp.objects.get(username=p1.username)
    j=u.utype
    id=3
    return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})

def delmed(request):
    p1=request.user
    n=MedInfo.objects.filter(puname=p1.username)
    u = SignUp.objects.get(username=p1.username)
    x = datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    j=u.utype
    id=5
    if request.method == "POST":
        mname=request.POST.get("id")
        uname=request.POST.get("uname")
        pname=request.POST.get("pname")
        address=request.POST.get("add")
        sup="none"
        qua=0
        price=0
        date=request.POST.get("date")
        expdate=request.POST.get("date")
        reqtype="deletemedicine"
        password=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=password):
            messages.info(request,'password is not valid')
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
        else:
            MedInfo.objects.filter(puname=uname,medname=mname).delete()
            t1=MedTrack(medname=mname,puname=uname,pname=pname,add=address,sup=sup,medquantity=qua,medprice=price,date=date,expdate=expdate,reqtype=reqtype)
            t1.save()
            messages.info(request,'Medicine Deleted')
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
    return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})

def updelmed(request):
    p1=request.user
    n=MedInfo.objects.filter(puname=p1.username)
    u = SignUp.objects.get(username=p1.username)
    x = datetime.datetime.now()
    now=x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d")
    j=u.utype
    id=4
    if request.method=="POST":
        mname=request.POST.get("id")
        uname=request.POST.get("uname")
        pname=request.POST.get("pname")
        address=request.POST.get("add")
        quantity=int(request.POST.get("quant"))
        date=request.POST.get("date")
        expdate=request.POST.get("exp")
        reqtype="updatedelmedicine"
        password=request.POST.get("pass")
        u1 = PharmacySignUp.objects.get(username=p1.username)
        if (u1.psw!=password):
            messages.info(request,'password is not valid')
            return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
        else:
            xin=MedInfo.objects.filter(puname=uname,medname=mname)
            for xin in xin:
                print(xin.medquantity)
            qua=int(xin.medquantity)-int(quantity)
            print(xin.medquantity,quantity,qua,"dskmcd")
            if(qua>=0):
                MedInfo.objects.filter(puname=uname,medname=mname).update(medquantity=qua)
                t1=MedTrack(medname=mname,puname=uname,pname=pname,add=address,sup=xin.sup,medquantity=quantity,medprice=xin.medprice,date=date,expdate=expdate,reqtype=reqtype)
                t1.save()
                messages.info(request,'Medicine quantity decreased')
                return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
            else:
                messages.info(request,'updated quantity< 0')
                return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})
    return render(request,"psmanage.html",{"id":id,"j":j,'n':n,"now":now})