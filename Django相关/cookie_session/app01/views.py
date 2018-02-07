from django.shortcuts import render,redirect
from .models import *

def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")

        ret=UserInfor.objects.filter(name=user,pwd=pwd)
        if ret:
            obj=redirect("/index/")
            obj.set_cookie("is_login",True,max_age=5)
            obj.set_cookie("user",user)
            return obj
    obj=render(request, "login.html")
    # obj.set_cookie()
    # obj.status_code=404
    return obj

def index(request):
    print(request.COOKIES)
    if not request.COOKIES.get("is_login"):
        return redirect("/login/")
    user=request.COOKIES.get("user")
    return render(request,"index.html",locals())

############################session 操作
def login_session(request):
    # import random
    # temp=""
    # for i in range(5):
    #     s=random.randint(0, 9)
    #     temp+=str(s)
    # s = temp
    # request.session["valid_code"]=s

    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")

        # valid=request.POST.get("valid")
        # if valid==request.session.get("valid_code"):
        #     return

        ret=UserInfor.objects.filter(name=user,pwd=pwd)
        if ret:
            # sessionID:h3ksm2h9ui4i72999mqdzm94vp0iql9u
            request.session["user"]=user
            '''
            if sessionID:h3ksm2h9ui4i72999mqdzm94vp0iql9u:更新
            1 创建随机字符串
            2 set_cookie("sessionID","123456")
            3 在django-session表添加记录
              session-key     session-data    
               123456         {"user":"alex"}
            '''
            return redirect("/index_session/")
    return render(request,"login.html")

def index_session(request):
    user=request.session.get("user")
    '''
    1  random_str=request.COOKIE.get("sessionID")
    2  在django-session表中过滤：
        obj=django-session.objects.filter(session-key=random_str).first()
    3  obj.session-data.get("user")
    '''
    if not user:
        return redirect("/login_session/")
    return render(request,"index.html",locals())

def logout(request):
    # sessionID:h3ksm2h9ui4i72999mqdzm94vp0iql9u
    request.session.flush()
    return redirect("/login_session/")