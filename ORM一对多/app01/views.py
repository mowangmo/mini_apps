from django.shortcuts import render,redirect,HttpResponse
from .models import *

def index(request):
    book_list=Book.objects.all()
    return render(request,"index.html",locals())

def add_book(request):
    if request.method=="POST":  #点击submit之后走这
        title=request.POST.get("title")
        price=request.POST.get("price")
        pub_date=request.POST.get("pub_date")
        publish_id=request.POST.get("publish_id")
        #  一对多的添加方式
        # 方式1：
        book_obj=Book.objects.create(title=title,price=price,publishDate=pub_date,publish_id=publish_id)
        # 方式2：
        # publish_obj=Publish.objects.filter(id=2).first()
        # book_obj=Book.objects.create(title=title, price=price, publishDate=pub_date,publish=publish_obj)
        return redirect("/index/")  #成功之后返回index
    publish_list=Publish.objects.all()      #为了渲染出版社
    return render(request,"add_book.html",locals())

def edit_book(request,edit_book_id):
    if request.method=="POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        Book.objects.filter(nid=edit_book_id).update(title=title,price=price,publishDate=pub_date,publish_id=publish_id)   #更新数据
        return redirect("/index/")
    edit_book=Book.objects.filter(nid=edit_book_id).first()
    publish_list = Publish.objects.all()
    return render(request,"edit_book.html",locals())

def del_book(request,del_book_id):
    Book.objects.filter(nid=del_book_id).delete()
    return redirect("/index/")

def query(request):
    book_obj=Book.objects.filter(nid=1).first()
    print(book_obj.title)
    print(book_obj.price)
    print(book_obj.publishDate)
    print(book_obj.publish_id)
    #print(book_obj.publish) # Publish object
    return HttpResponse("OK")