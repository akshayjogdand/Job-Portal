from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from AdminApp.models import UserInfo,UEmployment,UserEducation,Company,Industry,Payment,Job,Apply,Msg
import  datetime 
import random
from functions import handle_uploaded_file 
from django.core.mail import send_mail
from django.conf import settings

def homepage(request):
    comp1 = Company.objects.filter(type=1)
    comp2 = Company.objects.filter(type=2)
    comp3 = Company.objects.filter(type=3)
    comp4 = Company.objects.filter(type=4)
    comp6 = Company.objects.filter(type=6)
    comp7 = Company.objects.filter(type=7)
    comp8 = Company.objects.filter(type=8) 
    if("email" in request.session):
        user = UserInfo.objects.get(email =  request.session["email"] )
        cats = Industry.objects.all()

        msg = Msg.objects.filter(uname=user)
        msgdata = []
        value=0
        for i in msg:
            if(i.status == 1):
                value +=1
                msgdata.append(i)
        return render(request, "homepage.html",{"user" : user,"comp1" : comp1,"comp2" : comp2,"comp3" : comp3, "comp4" : comp4,"comp6" : comp6,"comp7" : comp7,"comp8" : comp8,"cats" : cats,"value":value,"msgdata":msgdata})
    elif("pwd" in request.session):
        user = Company.objects.get(password = request.session["pwd"])
        job = Job.objects.filter(company = user)
        list1 = []
        list2 = []
        count = 0
        for i in job:
            list2.append(i)
        list2.reverse()
        for i in list2:
            if( count == 5):
                break
            else:
                list1.append(i)
                count += 1
        return render(request,"rhome.html",{"user":user,"job" : list1})
    else:

        return render(request, "homepage.html",{"comp1" : comp1,"comp2" : comp2,"comp3" : comp3, "comp4" : comp4,"comp6" : comp6,"comp7" : comp7,"comp8" : comp8 })

def register(request):
    if(request.method=="GET"):
        return render(request,"register.html",{})
    else:
        u1 = UserInfo()
        u1.uname = request.POST["uname"]
        u1.email = request.POST["email"]
        u1.password = request.POST["pwd"]
        u1.phone = request.POST["phone"]
        u1.work_status = request.POST["work"]
        handle_uploaded_file(request.FILES['file'])
        u1.resume = request.FILES["file"]
        #u1.DOB = request.POST["dob"]
        try: 
            u1.save()
        except:
            messages.success(request, "Email already Register")
            return redirect(register)
        else:
            messages.success(request, "Register Sucessfully.")
            return redirect(homepage)

def login(request):
    try: 
        email = request.POST["email"]
        pswd =  request.POST["pwd"]
        user = UserInfo.objects.get(email = email,password=pswd)
    except:
        messages.success(request, "Invalid details. Please check the Email ID - Password combination.")
        return redirect(homepage)
    else:
        request.session["email"] = email
        return redirect(homepage)
        
def logout(request):
    request.session.clear()
    return redirect(homepage)

def update(request):
    cats = Industry.objects.all()

    try:
        email =  request.session["email"]
    except:
        return redirect(homepage)
    else:
        user = UserInfo.objects.get(email = email)
        msg = Msg.objects.filter(uname=user)
        msgdata = []
        value=0
        for i in msg:
            if(i.status == 1):
                value +=1
                msgdata.append(i)
        try:
            u1 = UEmployment.objects.filter(uname=user)
            try:
                u2 = UserEducation.objects.filter(uname=user)
            
            except:
                return render(request, "update.html",{"user" : user,"u1":u1,"cats":cats,"value":value,"msgdata":msgdata})
        except:
            return render(request, "update.html",{"user" : user,"cats":cats,"value":value,"msgdata":msgdata})
        else:
            return render(request, "update.html",{"user" : user,"u1":u1,"u2":u2,"cats":cats,"value":value,"msgdata":msgdata})

def updateResume(request):
    if(request.method=="POST"):
        if("email" in request.session):
            value = request.POST["action"]
            email =  request.session["email"]
            user = UserInfo.objects.get(email = email)
            handle_uploaded_file(request.FILES['file'])
            file = request.FILES["file"]
            user.resume = file
            user.save()
            messages.success(request, "Resume updated sucessfully.")
            return redirect(update)
    else:
        return redirect(login)
def changeProfile(request):
    
    if("email" in request.session):
        if(request.method=="POST"):
            handle_uploaded_file(request.FILES['photo'])
            value = request.FILES["photo"]
            email =  request.session["email"]
            user = UserInfo.objects.get(email = email)
            user.image = value
            user.save()
            messages.success(request, "Profile updated sucessfully.")
            return redirect(update)
    else:
        return redirect(login)
  
def updateHeadline(request):
    if("email" in request.session):
            if(request.method=="POST"):

                email =  request.session["email"]
                user = UserInfo.objects.get(email = email)
              
                headline =  request.POST["headline"]
                user.resume_headline = headline
                user.save()
                messages.success(request, "Resume headline updated sucessfully.")
                return redirect(update)
    else:
        return redirect(login)

def keySkills(request):

    if("email" in request.session):
        if(request.method=="POST"):

            email =  request.session["email"]
            user = UserInfo.objects.get(email = email)
            skills =  request.POST["skills"]
            user = UserInfo.objects.get(email = email)
            user.key_skills = skills
            user.save()
            messages.success(request, "Key skills updated sucessfully.")
        return redirect(update)
    else:
        return redirect(login)

def personal(request):
    if("email" in request.session):
        if(request.method=="POST"):
            u1 = UserInfo.objects.get(email = request.session["email"] )
            u1.uname = request.POST["uname"]
            u1.phone =  phone = request.POST["phone"]
            u1.address = request.POST["add"]
            u1.work_status = request.POST["work"]
            #u1.email = request.POST["email"]
            u1.save()
            messages.success(request, "Information updated sucessfully.")
            return redirect(update)
    else:
        return redirect(login)

def personalinfo(request):
    if("email" in request.session):
        if(request.method=="POST"):
            u1 = UserInfo.objects.get(email = request.session["email"] )
            dob = u1.DOB
            u1.gender = request.POST["gender"]
            u1.address = request.POST["add"]
            try:
                u1.DOB = request.POST["dob"]
                u1.save()
            except:
                u1.DOB = dob

                u1.save()
            messages.success(request, "Personal information updated sucessfully.")
            return redirect(update)
    else:
        return redirect(login)

def userExp(request):
    if("email" in request.session):
        if(request.method == "POST"):
            email = request.session["email"]
            u2 = UserInfo.objects.get(email=email)
            u1 = UEmployment()
            u1.uname = u2
            u1.cname =  request.POST["cname"]
            u1.designation = request.POST["desig"]
            u1.Join_date = request.POST["dt"]
            u1.salary =  request.POST["sal"]
            u1.profile = request.POST["pro"]
            u1.notice_period = request.POST["notice"]
            u1.save()
            print(u1)
            messages.success(request, "Exprience added sucessfully.")
            return redirect(update)
    else:
        return redirect(login)

def useredu(request): 
    if("email" in request.session):
        if(request.method == "POST"):
            email = request.session["email"]
            user = UserInfo.objects.get(email=email)
            try:
                user1 = UserEducation.objects.filter(uname = user)
            except:
                return redirect(update)
            for u in user1:
                if(u.education == request.POST["edu"]):
                    return redirect(update)
                    break
            else:
                u2 = UserEducation()
                u2.education = request.POST["edu"]
                u2.university = request.POST["inst"]
                u2.course = request.POST["course"]
                u2.marks = request.POST["mk"]
                u2.uname = user
                u2.year = request.POST["yr"]
                u2.save()
                messages.success(request, "Education added sucessfully.")
                return redirect(update)
    else:
        return redirect(login)

                
            
def editEdu(request,id):
    if("email" in request.session):
        if(request.method=="POST"):
            user = UserInfo.objects.get(email =  request.session["email"] )
            u1 = UserEducation.objects.get(uname=user,id = id)
            u1.education = request.POST["edu"]
            u1.institute = request.POST["inst"]
            u1.course = request.POST["course"]
            u1.marks = request.POST["mk"]
            u1.save()
            messages.success(request, "Education updated sucessfully.")
            return redirect(update)
    else:
        return redirect(login)
        


def delete(request):
    user = Apply.objects.all()
    for u1 in user:
        u1.delete()


def editExp(request,id):
    if("email" in request.session):
        if(request.method=="POST"):
                user = UserInfo.objects.get(email = request.session["email"])
                u1 = UEmployment.objects.get(uname = user,id = id)
                date = u1.Join_date
                notice = u1.notice_period 
                u1.cname =  request.POST["cname"]
                u1.designation = request.POST["desig"]
                
                u1.salary =  request.POST["sal"]
                u1.profile = request.POST["pro"]
                try:
                    u1.Join_date = request.POST["dt"]
                    u1.notice_period = request.POST["notice"]
                    u1.save()
                except:
                    u1.Join_date  = date
                    u1.notice_period  = notice
                    u1.save()
                messages.success(request, "Experience updated sucessfully.")
                return redirect(update)
    else:
        return redirect(login)
        

def deleteExp(request,id):
    if("email" in request.session):
        user = UserInfo.objects.get(email = request.session["email"])
        user = UEmployment.objects.get(uname = user,id = id)
        user.delete()
        messages.success(request, "Experience deleted sucessfully.")
        return redirect(update)
    else:
        return redirect(login)

def rcruitSignup(request):
    if(request.method=="GET"):
        type = Industry.objects.all()
        return render(request,"rsignup.html",{"type" : type})
    else:
        c1 = Company()
        cname = request.POST["cname"]
        c1.cname = cname
        c1.email = request.POST["email"]
        c1.phone = request.POST["phone"]
        c1.person = request.POST["person"]
        c1.pincode = request.POST["pin"]
        c1.address1 = request.POST["add"]
       # handle_uploaded_file(request.FILES['profil'])
        #profile =request.FILES['profil']
        handle_uploaded_file(request.FILES['file1'])
        c1.image1 = request.FILES["file1"]
        c1.expiry_date = datetime.datetime.now() + datetime.timedelta(days = 365)
        type = request.POST["type"]
        value = Industry.objects.get(type = type)
        c1.type = value
        try:
            c1.save()
            request.session["cname"] = cname
        except:
            messages.success(request, "Email already Register")
            return redirect(rcruitSignup)
        else:
            messages.success(request, "Register sucessfully")
            return redirect(subscribe)

def rcruitLogin(request):
    if(request.method == "GET"):
        return render(request,"rlogin.html",{})
    else:
        email = request.POST["email"]
        pwd = request.POST["pwd"]
        try: 
            user = Company.objects.get(email = email,password=pwd)
        except:
            messages.success(request, "Invalid details. Please check the Email ID - Password combination.")
            return render(request,"rlogin.html",{})
        else:
            request.session["pwd"] = pwd
            messages.success(request, "Login Sucessfully.")
            return redirect(homepage)


def ChangePass(request):
    if("pwd" in request.session):
        if(request.method=="GET"):
            return render(request,"ChangePass.html",{})
        else:
            pwd = request.POST["pwd"]
            pwd1 = request.POST["pwd1"]
            pwd2 = request.POST["pwd2"]
            try:
                user = Company.objects.get(password = pwd)
            except:
                messages.success(request, "Incorrect Existing Password ")
                return redirect(ChangePass)
            else:
                if(pwd1 == pwd2):
                 
                    user.password = pwd1
                    user.save()
                    request.session.clear()
                    request.session["pwd"] = pwd1
                    messages.success(request, "Password changes sucessfully. ")
                    return redirect(homepage)
                else:
                    messages.success(request, "Password not match ")
                    return redirect(ChangePass)
    else:
        return redirect(homepage)

                  
def EditData(request):
    if("pwd" in request.session):
        user = Company.objects.get(password = request.session["pwd"])
        img = user.image1
        print(img)
        if(request.method=="GET"):
            return render(request,"EditData.html",{"user" : user})
        else:
            user.phone = request.POST["phone"]
            user.person = request.POST["person"]
            user.pincode = request.POST["pin"]
            user.address1 = request.POST["add"]
  
            try:
                handle_uploaded_file(request.FILES['file'])
                user.image1 = request.FILES["file"]
                user.save()
            except:
                user.image1 = img
                user.save()

            messages.success(request, "Profile updated sucessfully. ")
            return redirect(homepage)
    else:
        return redirect(homepage)
          

def subscribe(request):
    if("cname" in request.session):
        if(request.method=="GET"):
            return render(request,"subscribe.html",{})
        else:
            value = request.POST["action"]
            cname = request.session["cname"]
            user = Company.objects.get(cname= cname)
            if(value == "hot"):
                x = 8000
                user.plan = "Standard"
                user.post = 300
                user.save()
                return render(request, "payment.html",{"x" : x})
            else:
                x = 5000
                user.plan = "Regular"
                user.post = 100
                user.save()
                return render(request, "payment.html",{"x" : x})
    else:
        return redirect(homepage)
    

def payment(request):
    if("cname" in request.session):   

        if(request.method == "POST"):
            cardno = request.POST["cardno"]
            cvv = request.POST["cvv"]
            expiry = request.POST["exp"]
            pay = request.POST["payment"]
            try:
                buyer = Payment.objects.get(cardno=cardno,cvv=cvv,expiry=expiry)
            except:
                messages.success(request, "Invalid Details. ")
                return render(request, "payment.html",{"x" : pay})
            else:
                value = request.session["cname"]
                user = Company.objects.get(cname = value)
                owner = Payment.objects.get (cardno='1111',cvv='111',expiry='12/2024')
                owner.balance +=  int(pay)
                buyer.balance -= int(pay)
                owner.save()
                buyer.save()
                pass1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','!','@','#','$']
                password = ""
                for x in range(7):
                    password = password + random.choices(pass1)[0]
                    user.password = password
                    user.save()
                    request.session.clear()

                return render(request,"success.html",{"pass" : password})
        else:
            return render(request,"payment.html",{})
    else:
        return redirect(homepage)
def addJob(request):
    if("pwd" in request.session):
        user = Company.objects.get(password =  request.session["pwd"])
        if(request.method == "GET"):
            return render(request,"addjob.html",{})
        else:
            j1 = Job()
            j1.title = request.POST["title"]
            j1.description = request.POST["description"]
            j1.Experience =  request.POST["experience"]
            j1.salary = request.POST["salary"]
            j1.Education = request.POST["education"]
            j1.no_opening = request.POST["nof"]
            j1.skills = request.POST["skills"]
            j1.company = user
            user.post = user.post-1
            user.save()
            j1.save()
            return redirect(homepage)
    return redirect(homepage)
    
def sub(request):
    if("pwd" in request.session):
        user = Company.objects.get(password =  request.session["pwd"])
        return render(request,"sub.html",{"user" : user})
    else:
        return redirect(homepage)  

def records(request):
    if("pwd" in request.session):
        user = Company.objects.get(password =  request.session["pwd"])
        jobs  = Job.objects.filter(company = user)
        if(not jobs):
            return render(request,"records1.html",{"user" : user})
        else:
            return render(request,"records.html",{"jobs" : jobs,"user" : user})
    else:
        return redirect(homepage)

def deletejob(request,id):
    if("pwd" in request.session):
        user = Company.objects.get(password =  request.session["pwd"])
        j1 = Job.objects.get(id = id)
        j1.delete()
        return redirect(records)


def editjob(request,id):
    if("pwd" in request.session):
        user = Company.objects.get(password =  request.session["pwd"])
        j1 = Job.objects.get(id = id)
        j1.opn =  j1.no_opening
        j1.title = request.POST["title"]
        j1.description = request.POST["description"]
        j1.Experience =  request.POST["experience"]
        j1.salary = request.POST["salary"]
        j1.Education = request.POST["education"]
        j1.skills = request.POST["skills"]
        j1.company =user

        try:
            j1.no_opening = request.POST["nof"]
            j1.save()
        except:
            j1.no_opening = j1.opn
            j1.save()
        return redirect(homepage)
    return redirect(homepage)
    
def searchJob(request):
    title = request.POST["title1"]
    loc = request.POST["loc1"]
    cats = Industry.objects.all()

    if(len(loc) == 0 and len(title)!= 0 ):
        job = Job.objects.filter(title = str(title))
        print(job)
        if("email" in request.session):
            user = UserInfo.objects.get( email = request.session["email"])
            msg = Msg.objects.filter(uname=user)
            msgdata = []
            value=0
            for i in msg:
                if(i.status == 1):
                    value +=1
                    msgdata.append(i)
            if(not job):
                return render(request,"searchmsg.html",{"cats":cats,"user":user,"value":value,"msgdata":msgdata})
            else:
                return render(request,"search1.html",{"job" : job,"cats":cats,"user":user,"value":value,"msgdata":msgdata})
        else:
            if(not job):
                return render(request,"searchmsg.html",{})
            else:
                return render(request,"search1.html",{"job" : job})
    elif(len(title)== 0 and len(loc) != 0 ):
        comp = Company.objects.filter(address1 = loc)
        list1 = []
        for i in comp:
            job = Job.objects.filter(company_id = i)
            list1.append(job)
        list2 = []
        for j in list1:
            for job in j:
                list2.append(job)
        if("email" in request.session):
            user = UserInfo.objects.get( email = request.session["email"])
            msg = Msg.objects.filter(uname=user)
            msgdata = []
            value=0
            for i in msg:
                if(i.status == 1):
                    value +=1
                    msgdata.append(i)
            if(not list1):
                return render(request,"searchmsg.html",{"cats":cats,"user":user,"value":value,"msgdata":msgdata})
            else:
                return render(request,"search1.html",{"job" : list2,"cats":cats,"user":user,"value":value,"msgdata":msgdata})
        else:
            if(not list1):
                return render(request,"searchmsg.html",{})
            else:
                return render(request,"search1.html",{"job" : list2})

    elif(len(loc) != 0 and len(title)!= 0):
        list1 = []
        job = Job.objects.filter(title = title)
        for i in job:
            comp = Company.objects.filter(address1 = loc,id=i.company_id)
            list1.append(i)
        if("email" in request.session):
            user = UserInfo.objects.get( email = request.session["email"])
            msg = Msg.objects.filter(uname=user)
            msgdata = []
            value=0
            for i in msg:
                if(i.status == 1):
                    value +=1
                    msgdata.append(i)
            if(not list1):
                return render(request,"searchmsg.html",{"cats":cats,"user":user,"value":value,"msgdata":msgdata})
            else:
                return render(request,"search1.html",{"job" : list1,"cats":cats,"user":user,"value":value,"msgdata":msgdata})
        else:
            if(not list1):
                return render(request,"searchmsg.html",{})
            else:
                return render(request,"search1.html",{"job" : list1})


def jobcat(request,id):
    cats = Industry.objects.all()
    comp8 = Company.objects.filter(type=id) 

    list1 = []
    for i in comp8:
        print(i)
        jobs = Job.objects.filter(company_id = i)
        list1.append(jobs)
    if("email" in request.session):
            user = UserInfo.objects.get( email = request.session["email"])
            msg = Msg.objects.filter(uname=user)
            msgdata = []
            value=0
            for i in msg:
                if(i.status == 1):
                    value +=1
                    msgdata.append(i)
            return render(request,"jobcat.html",{"jobs" : list1,"cats":cats,"user" : user,"value":value,"msgdata":msgdata})
    else:
        return render(request,"jobcat.html",{"jobs" : list1})

def jobdetails(request,id):
    cats = Industry.objects.all()
    job = Job.objects.get(id = id)
    if("email" in request.session):
        user = UserInfo.objects.get( email = request.session["email"])
        msg = Msg.objects.filter(uname=user)
        msgdata = []
        value=0
        for i in msg:
            if(i.status == 1):
                value +=1
                msgdata.append(i)
        try:
            apply = Apply.objects.get(job=job,uname=user)
        except:
            return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"value":value,"msgdata":msgdata})
        else:
            status = apply.status
            return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"status":status,"value":value,"msgdata":msgdata})
    else:
        return render(request,"jobdetails.html",{"job" : job})

def loginone(request,id):
    cats = Industry.objects.all()

    try: 
        email = request.POST["email"]
        pswd =  request.POST["pwd"]
        job = Job.objects.get(id = id)
        user = UserInfo.objects.get(email = email,password=pswd)
        msg = Msg.objects.filter(uname=user)
        msgdata = []
        value=0
        for i in msg:
            if(i.status == 1):
                value +=1
                msgdata.append(i)
    except:
        messages.success(request, "Invalid details. Please check the Email ID - Password combination.")
        return render(request,"jobdetails.html",{"job" : job,"cats":cats})
    else:
        request.session["email"] = email
        messages.success(request, "Login Sucessfully..!!!")
        try:
            apply = Apply.objects.get(job=job,uname=user)
        except:
            return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"value":value,"msgdata":msgdata})
        else:
            status = apply.status
            return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"status":status,"value":value,"msgdata":msgdata})
    
def apply(request,id):
    user = UserInfo.objects.get( email = request.session["email"])
    msg = Msg.objects.filter(uname=user)
    msgdata = []
    value=0
    for i in msg:
        if(i.status == 1):
            value +=1
            msgdata.append(i)

    cats = Industry.objects.all()
    job = Job.objects.get(id = id)
    company = Company.objects.get(job= job)
    a1 = Apply()
    a1.uname = user
    a1.job = job
    a1.status = "APPLIED"
 

    try:
        apply = Apply.objects.get(job=job,uname=user)
    except:
        a1.save()
        apply = Apply.objects.get(job=job,uname=user)
        status = apply.status
        #print(status)
        job.response = job.response + 1
        job.save()
        messages.success(request, "Apply Sucessfully.")
        return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"status":status,"value":value,"msgdata":msgdata})
    else:
        apply = Apply.objects.get(job=job,uname=user)
        status = apply.status
        #print(status)
        messages.success(request, "Apply Sucessfully.")
        return render(request,"jobdetails.html",{"job" : job,"cats":cats,"user" : user,"status":status,"value":value,"msgdata":msgdata})

        


def history(request,id):
    user = UserInfo.objects.get(email =  request.session["email"] )
    msg = Msg.objects.filter(uname=user)
    msgdata = []
    value=0
    for i in msg:
        if(i.status == 1):
            value +=1
            msgdata.append(i)
    cats = Industry.objects.all()
    user = UserInfo.objects.get(id = id)
    app = Apply.objects.filter(uname=user)
    if(not app):
        return render(request,"historymsg.html",{"cats":cats,"user":user,"value":value,"msgdata":msgdata})
    else:
        return render(request,"history.html",{"app":app,"cats":cats,"user":user,"value":value,"msgdata":msgdata})


def resp(request,id):
    if("pwd" in request.session):
        company = Company.objects.get(password = request.session["pwd"])
        job = Job.objects.get(id = id)
        try:
            app = Apply.objects.filter(job = job)
            print(app)
        except:
            return redirect(homepage)
        else:
            if(not app):
                return  render(request,"response1.html",{"job":job})  
            else:
                return  render(request,"response.html",{"app":app,"job":job})

def viewprofile(request,id):
    user = UserInfo.objects.get(id = id)
    try:
        u1 = UEmployment.objects.filter(uname=user)
        try:
            u2 = UserEducation.objects.filter(uname=user)
        except:
            return render(request, "viewprofile.html",{"user" : user,"u1":u1})
    except:
        return render(request, "viewprofile.html",{"user" : user})
    else:
        return render(request, "viewprofile.html",{"user" : user,"u1":u1,"u2":u2})
    
def sendmsg(request,id):
    if("pwd" in request.session):
        company = Company.objects.get(password = request.session["pwd"])
        user = UserInfo.objects.get(id = id)
        msg = request.POST["msg"]
        job1 = request.POST["job"]
        job = Job.objects.get(id = job1)
        m1 = Msg()
        m1.company = company
        m1.uname = user
        m1.msg= msg
        m1.job = job 
        app = Apply.objects.filter(job = job)
        try:
            msg = Msg.objects.get(uname=user,job=job)
        except:
            m1.save()
            messages.success(request, "Message Sent Sucessfully to "+user.uname+".")
            return  render(request,"response.html",{"app":app,"job":job})
        else:
            messages.success(request, "Message already sent to "+user.uname+".")
            return  render(request,"response.html",{"app":app,"job":job})
    

def openmsg(request,id):
    user = UserInfo.objects.get(email =  request.session["email"] )
    msg= Msg.objects.get(id = id)
    msg.status = 0
    msg.save()
    msgs = Msg.objects.filter(uname=user)
    msgdata = []
    value=0
    for i in msgs:
        if(i.status == 1):
            value +=1
            msgdata.append(i)
    cats = Industry.objects.all()

    return render(request,"openmsg.html",{"msg":msg,"cats":cats,"user":user,"value":value,"msgdata":msgdata})

def inbox(request):
    if("email" in request.session):
        user = UserInfo.objects.get( email = request.session["email"])
        msgs = Msg.objects.filter(uname = user)
        msgdata = []
        value=0
        for i in msgs:
            if(i.status == 1):
                value +=1
                msgdata.append(i)
        cats = Industry.objects.all()
        if(not msgs):
            return render(request,"inbox1.html",{"cats":cats,"user":user,"value":value,"msgdata":msgdata})
        else:
            return render(request,"inbox.html",{"msgs":msgs,"cats":cats,"user":user,"value":value,"msgdata":msgdata})

def send(request,id):
    if("pwd" in request.session):
        company = Company.objects.get(id = id)
        print(company.cname)
        msgs = Msg.objects.filter(company = company)
        if(not msgs):
        
            return render(request, "sendbox.html",{"user" : company})
        else:
            return render(request, "sendbox1.html",{"msgs":msgs})


def forget(request):
    return render(request,"forget.html",{})

def aboutus(request):
    return render(request,"about.html",{})

def contact(request):
    return render(request,"contact.html",{})

def resetpass(request):
    email = request.POST["email"]
    try:
        user = UserInfo.objects.get(email =email)
    except:
        return redirect(homepage)
    else:
        msg = """
            Hello 
            To change the password 
            click below link
            http://127.0.0.1:8000/newpass
            Thank You,
            Job Portal Community.
            """
            #below code is used for sending mail
        send_mail("Welcome to Job Portal",msg,'settings.EMAIL_HOST_USER',[email],fail_silently=False)
        return redirect(homepage)
            #after signup direct user can see login page

def newpass(request):
    return render(request,"newpass.html",{})

def userpass(request):
    email = request.POST["email"]
    pwd = request.POST["pwd"]
    
    try:
        user = UserInfo.objects.get(email =email)
    except:
        messages.success(request, " Incorrect Email id.")
        return redirect(homepage)
    else:
        user.password = pwd
        user.save()
        messages.success(request, "Password changes Sucessfully.")
        return redirect(homepage)
        

