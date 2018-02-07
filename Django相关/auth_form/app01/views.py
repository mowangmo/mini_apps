from django.shortcuts import render,redirect

# Create your views here.
from django.contrib import auth


def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        print("user:",request.user)
        user=auth.authenticate(username=user,password=pwd)
        if user:
            auth.login(request,user)#request.session["user_id"]=user.id
            print("user2:", request.user)

            return redirect("/index/")

    return render(request, "login.html")

def index(request):

    user=request.user
    # if not user.id:
    #     return redirect("/login/")

    #if not user.is_authenticated():return redirect("/login/")


    username=user.username
    return render(request,"index.html",locals())

def logout(request):
    auth.logout(request)
    return redirect("/login/")

from django.contrib.auth.models import User
def reg(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        user=User.objects.create_user(username=user,password=pwd)
        return redirect("/login/")

    return render(request,"reg.html")