from django.shortcuts import render,HttpResponse
from .models import  *
import json

def index(reqeust):
    import time
    # time.sleep(10)
    return render(reqeust,"index.html")

def ajax_handle1(request):
    # import time
    # time.sleep(10)
    response={"state":True}
    import json
    return HttpResponse(json.dumps(response))

def ajax_handle2(request):
    num1=request.POST.get("num1")
    num2=request.POST.get("num2")
    ret=int(num1)+int(num2)
    return HttpResponse(str(ret))

def login(request):
    return render(request,"login.html")

def ajax_login(request):
    response = {"is_login": False, "error_msg": ""}
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    ret = User.objects.filter(user=user, pwd=pwd)
    if ret:
        response["is_login"] = True
    else:
        response["error_msg"] = "user or pwd error !!!"
    print('-----------',user,pwd,response)
    return HttpResponse(json.dumps(response))

def home(request):
    return render(request,"home.html")
