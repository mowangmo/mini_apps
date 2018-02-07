from django.shortcuts import render,HttpResponse
from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError

class LoginForm(forms.Form):
    user=forms.CharField(label="用户名",min_length=3,max_length=8,
                         widget=widgets.TextInput(attrs={"class": "form-control"}),
                         error_messages={"min_length":"太短","required":"必填"})

    pwd=forms.CharField(label="密码",min_length=5,
                        widget=widgets.PasswordInput(attrs={"class":"form-control"}),
                        error_messages={"min_length":"太短", "required": "必填"}
                        )

    def clean_user(self):
        val=self.cleaned_data.get("user")

        import re
        # if not UserInfo.objects.filter(username=val):
        #     return val
        # else:
        #     raise ValidationError("")

        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字！")

    def clean_pwd(self):
        val=self.cleaned_data.get("pwd")

        if val.startswith("yuan"):
            return val
        else:
            raise ValidationError("没有yuan开头")

    # email=forms.EmailField()
    # age=forms.IntegerField()

def login(request):
    if request.method=="POST":
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data)  # {"user":"","pwd":123}
            return HttpResponse("OK")
        else:
            # print(login_form.cleaned_data)# {"pwd":123456}
            # print(type(login_form.errors)) # {"user":["","",]}
            # print(type(login_form.errors.get("user"))) # {"user":"....."}
            return render(request, "login_form.html", locals())

    login_form=LoginForm()
    return render(request,"login_form.html",locals())