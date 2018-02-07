from django.shortcuts import render,redirect,HttpResponse
from .models import *

def index(request):
    book_list=Book.objects.all()
    return render(request,"index.html",locals())

def add_book(request):
    if request.method=="POST":
        title=request.POST.get("title")
        price=request.POST.get("price")
        pub_date=request.POST.get("pub_date")
        publish_id=request.POST.get("publish_id")

        #  一对多的添加方式
        # 方式1：
        #book_obj=Book.objects.create(title=title,price=price,publishDate=pub_date,publish_id=publish_id)
        # 方式2：
        # publish_obj=Publish.objects.filter(id=2).first()
        # book_obj=Book.objects.create(title=title, price=price, publishDate=pub_date,publish=publish_obj)

        #  多对多关系的创建
        book_obj = Book.objects.create(title=title, price=price, publishDate=pub_date, publish_id=publish_id)

        print("==",book_obj.authors.all()) # <QuerySet []>

        # add 方法 绑定多对多的关系
        #jing = Author.objects.filter(name="景丽洋").first()
        #alex = Author.objects.filter(name="alex").first()
        #book_obj.authors.add(jing,alex)
        #book_obj.authors.add(*[jing,alex])
        #author_list=Author.objects.filter(age__gt=20)
        #book_obj.authors.add(*author_list)
        # remove 方法 绑定多对多的关系
        book_obj=Book.objects.get(nid=9)
        #alex = Author.objects.filter(name="alex").first()
        #book_obj.authors.remove(alex)
        book_obj.authors.clear()

        #print("==", book_obj.authors.all())

        # 失败的原因：找不到第三张关系表的名字
        # book_authors.objects.create(book_id=book_obj.id,author_id=jing.id)
        # book_authors.objects.create(book_id=book_obj.id,author_id=alex.id)
        return redirect("/index/")

    publish_list=Publish.objects.all()
    return render(request,"add_book.html",locals())

def edit_book(request,edit_book_id):
    if request.method=="POST":
        Book.objects.filter(nid=edit_book_id).update()
        return redirect("/index/")
    edit_book=Book.objects.filter(nid=edit_book_id).first()
    publish_list = Publish.objects.all()
    return render(request,"edit_book.html",locals())

def query(request):
    #######################基于model对象查询##########################
    # 一对多的查询
    # 查询java的出版社的邮箱(正向查询：按字段book_obj.publish)
    # book_obj=Book.objects.filter(title="java").first()
    # print(book_obj.publish.email)
    # 查询人民出版社出版过的所有的书籍名称（反向查询：按表名小写_set  publish_obj.book_set）
    # publish_obj=Publish.objects.filter(name="人民出版社").first()
    # print("---",publish_obj.book_set.all())

    # 多对多的查询
    # 查询php这本书籍的所有作者的名字以及年龄(正向查询：按字段book_obj.authors)
    # book_obj=Book.objects.filter(title="php").first()
    # print(book_obj.authors.all())
    # for obj in book_obj.authors.all():
    #     print(obj.name,obj.age)

    # 查询alex出版社过的所有书籍的名称和价格
    # alex=Author.objects.filter(name="alex").first()
    # print(alex.book_set.all())
    # for obj in alex.book_set.all():
    #     print(obj.title,obj.price)

    # 一对一查询
    # 查询tel=789的作者的名字  正向查询按字段
    # ad=AuthorDetail.objects.filter(tel="789").first()
    # print(ad.author.name)
    #
    # # 查询alex的手机号是多少
    # alex=Author.objects.filter(name='alex').first()
    # print(alex.authordetail.tel) # 789

    #######################基于QuerySet和__ 查询##########################
    # 一对多的查询
    # 查询java的出版社的邮箱(正向查询：按字段book_obj.publish)    [obj1,obj2,...]
    # ret=Book.objects.filter(nid__gt=6).values("publish__name")
    # print(ret)
    # 查询人民出版社出版过的所有的书籍名称
    # ret=Publish.objects.filter(name="人民出版社").values("book__title")
    # print(ret)

    # 多对多的查询
    # 查询php这本书籍的所有作者的名字以及年龄
    # ret=Book.objects.filter(title="php").values("authors__name","authors__age")
    # print(ret)
    # 查询alex出版社过的所有书籍的名称和价格
    # ret=Author.objects.filter(name="alex").values("book__title","book__price")
    # print(ret)
    # 一对一查询
    # 查询tel=789的作者的名字
    # ret=AuthorDetail.objects.filter(tel="789").values("author__name")
    # # 查询alex的手机号是多少
    # ret=Author.objects.filter(name="alex").values("authordetail__tel")

    ####################################
    #查询人民出版社出版过的所有的书籍名称
    #查询书籍
    # ret=Publish.objects.filter(name="人民出版社").values("book__title")
    # ret=Book.objects.filter(publish__name="人民出版社").values("title")

    # 手机号以151开头的作者出版过的所有书籍名称以及出版社名称

    # ret=Book.objects.filter(authors__authordetail__tel__startswith="7").values("title","publish__name")
    # print(ret)

    #######################聚合查询##########################
    # 聚合函数  aggregate
    from django.db.models import Sum,Count,Max,Min,Avg
    # ret=Book.objects.all().aggregate(Sum("price"))
    # print(ret)

    # 分组函数 annotate
    # 查询每一个出版社出版社出版的书籍个数
    # ret=Publish.objects.all().annotate(c=Count("book__title")).values("name","c")
    # print(ret) # <QuerySet [<Publish: 人民出版社>, <Publish: 机械出版社>, <Publish: 北京出版社>]>

    # 查询每一本书的作者个数
    #ret=Book.objects.all().annotate(author_num=Count("authors")).values("author_num","title")
    # ret=Book.objects.all().annotate(author_num=Count("authors")).filter(author_num__gt=0)
    # print(ret)

    ##########################F Q

    #查询 2018-01-09出版的且价格大于150的书籍
    # ret=Book.objects.filter(publishDate="2018-01-09",price__gt=150)
    # print(ret)

    # 评论数大于点赞数的书籍
    from django.db.models import F ,Q
    # ret=Book.objects.filter(poll_num__gt=F("commnet_num")*2)
    # print(ret)
    #Book.objects.all().update(price=F("price")+100)
    # 查询 2018-01-09出版的或者价格大于150的书籍
    # ret=Book.objects.filter(Q(publishDate="2018-01-17")&~Q(price__gt=300))
    # print(ret)
    return HttpResponse("OK")