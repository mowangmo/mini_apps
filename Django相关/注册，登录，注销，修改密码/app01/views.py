from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method=="POST":
        user=request.POST.get("user")
        pwd=request.POST.get("pwd")
        user=auth.authenticate(username=user,password=pwd)
        if user:
            auth.login(request,user)    #request.session["user_id"]=user.id
            return redirect("/index/")
    return render(request, "login.html")

def index(request):
    user=request.user
    username=user.username
    return render(request,"index.html",locals())

def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required
def cpass(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                return redirect("/login/")
        else:
            state = 'password_error'
    content = {
        'user': user,
        'state': state,
    }
    print(content)
    return render(request, 'change_pass.html', content)

class RegForm(forms.Form):
    user=forms.CharField(label="登录名称",min_length=4,max_length=16,
                         widget=widgets.TextInput(attrs={"class": "form-control" ,"id":"user" ,"placeholder": "登录用户名，不少于4个字符"}),
                         error_messages={"min_length":"太短","required":"必填"})

    pwd=forms.CharField(label="密  码",min_length=6,
                        widget=widgets.PasswordInput(attrs={"class":"form-control","id":"pwd","placeholder": "密码至少6位"}),
                        error_messages={"min_length":"太短", "required": "必填"})

    pwd2=forms.CharField(label="确认密码",min_length=6,
                          widget=widgets.PasswordInput(attrs={"class": "form-control","id": "pwd2", "placeholder": "请输入确认密码"}),
                          error_messages={"min_length": "太短", "required": "必填"})

    email=forms.EmailField(label="邮  箱",
                           widget=widgets.TextInput(attrs={"class": "form-control" ,"id":"email", "placeholder": "请输入邮箱账号"}),
                           error_messages={"email": "邮箱格式错误", "required": "必填"})        #自定义中文报错

    phone=forms.CharField(label="手机号",min_length=11,
                          widget=widgets.TextInput(attrs={"class": "form-control", "id": "phone", "placeholder": "请输入手机号"}),
                          error_messages={"min_length": "手机号码有误！", "required": "必填"})

    def clean_user(self):
        val=self.cleaned_data.get("user")
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字！")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        pwd2 = self.cleaned_data.get("pwd2")
        print(pwd,pwd2)
        if pwd == pwd2:     
            return self.cleaned_data
        else:
            raise ValidationError("确认密码错误！")

    def clean_phone(self):
        val=self.cleaned_data.get("phone")
        if val.isdigit():
            return val
        else:
            raise ValidationError("手机号码有误！")

def reg(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            print(reg_form.cleaned_data)  # {"user":"","pwd":123}
            user = request.POST.get("user")
            pwd = request.POST.get("pwd")
            user = User.objects.create_user(username=user, password=pwd)
            return redirect("/login/")
        else:
            return render(request, "reg_form.html", locals())
    reg_form = RegForm()
    return render(request, "reg_form.html", locals())

