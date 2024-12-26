from django.shortcuts import render,HttpResponse,redirect
from django .contrib.auth import authenticate,logout,login
from .models import User,Student,Teacher

# Create your views here.


def home(request):
    return render(request,"home.html",)

def student_register(request):
    if request.method=="POST":
        f=request.POST['Firstname']
        l=request.POST['Lastname']
        e=request.POST['Email']
        u=request.POST['username']
        p=request.POST['password']
        a=request.POST['address']
        ph=request.POST['phone_number']
        g=request.POST['guardian']
        new_user=User.objects.create_user(first_name=f,last_name=l,email=e,username=u,password=p,
        usertype='student',is_active=False)
        new_user.save()
        x=Student.objects.create(student_id=new_user,guardian=g,address=a,Phone_number=ph)
        x.save()
        return redirect("logins")
    else:
        return render(request,'studentregister.html')


def teacher_register(request):
    if request.method=="POST":
        f=request.POST['Firstname']
        l=request.POST['Lastname']
        e=request.POST['Email']
        u=request.POST['username']
        p=request.POST['password']
        a=request.POST['address']
        ph=request.POST['phone_number']
        s=request.POST['salary']
        ex=request.POST['experience']

        new_user=User.objects.create_user(first_name=f,last_name=l,email=e,username=u,password=p,
        usertype='teacher',is_active=True,is_staff=True)
        new_user.save()
        x=Teacher.objects.create(teacher_id=new_user,experience=ex,salary=s,address=a,phone_number=ph)
        x.save()
        return redirect("logins")
    else:
        return render(request,'teacherregister.html')

def logins(request):
    if request.method=="POST":
        u=request.POST["username"]
        p=request.POST["password"]
        userpass=authenticate(request,username=u,password=p)
        if userpass is not None and userpass.is_superuser==1:
            return redirect('adminhome')
        elif userpass is not None and userpass.is_staff==1:
            login(request,userpass)
            request.session['teacher_id']=userpass.id
            return redirect('teacherhome')
        elif userpass is not None and userpass.is_active==1:
            login(request,userpass)
            request.session['student_id']=userpass.id
            return redirect('studenthome')
        else:
            return HttpResponse("inavlid login")
    else:
        return render(request,'login.html')


def adminhome(request):
    return render(request,'adminhome.html')

def viewteacher(request):
    x=Teacher.objects.all()
    return render(request,"viewteacher.html",{"data":x})

def deleteteacher(request):
    x=Teacher.objects.all()
    return render(request,"deleteteacher.html",{"data":x})

def delteacher(request,id):
    x=Teacher.objects.get(id=id)
    x.delete()
    return redirect("delteacher")

def viewstudent(request):
    x=Student.objects.all()
    return render(request,"viewstudent.html",{"data":x})

def approvestudent(request):
    x=Student.objects.all()
    return render(request,"approvestudent.html",{"data":x})

def approve(request,id):
    x=User.objects.get(id=id,usertype='student')
    x.is_active=True
    x.save()
    return redirect("approvestudent")

def deletestudent(request):
    x=Student.objects.all()
    return render(request,"deletestudent.html",{"data":x})

    

def delstudent(request,id):
    x=Student.objects.get(id=id)
    x.delete()
    return redirect("deletestudent")


def studenthome(request):
    return render(request,"studenthome.html")


def editstudent(request):
    x=request.session['student_id']
    y=Student.objects.get(student_id=x)
    return render(request,"editstudent.html",{"data":y})

def updatestudent(request,id):
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        a=request.POST['address']
        ph=request.POST['phone']
        g=request.POST['guardian']
        x=Student.objects.get(id=id)
        x.address=a
        x.Phone_number=ph
        x.guardian=g
        x.save()
        y=User.objects.get(id=id)
        y.first_name=f
        y.last_name=l
        y.email=e
        y.save()
        return HttpResponse("Updated Successfully")
    else:
        return render(request,"editstudent.html")
    
def hometeacher(request):
    x=Teacher.objects.all()
    return render(request,"hometeacher.html",{"data":x})


def logoutstudent(request):
    logout(request)
    return redirect('home')


        
def teacherhome(request):
    return render(request,"teacherhome.html")

def editteacher(request):
    x=request.session["teacher_id"]
    y=Teacher.objects.get(teacher_id=x)
    return render(request,"editteacher.html",{"data":y})

def updateteacher(request,id):
    if request.method=="POST":
        f=request.POST['fname']
        l=request.POST['lname']
        e=request.POST['email']
        a=request.POST['address']
        ph=request.POST['phone']
        s=request.POST['salary']
        ex=request.POST['experience']
        x=Teacher.objects.get(id=id)
        x.address=a
        x.phone_number=ph
        x.salary=s
        x.experience=ex
        x.save()
        y=User.objects.get(id=id)
        y.first_name=f
        y.last_name=l
        y.email=e
        y.save()
        return HttpResponse("Updated Successfully")
    else:
        return render(request,"editteacher.html")
    

def logoutteacher(request):
    logout(request)
    return redirect("home")


def index(request):
    return render(request,"index.html")