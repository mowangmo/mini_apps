from django.db import models

class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    read_num=models.IntegerField(default=0)
    commnet_num=models.IntegerField(default=0)
    poll_num=models.IntegerField(default=0)
    # publish：与当前书籍对象关联的的出版社对象
    publish=models.ForeignKey(to="Publish",to_field="id")
    # authors： 与当前书籍关联的所有作者的集合
    authors=models.ManyToManyField(to="Author")
    def __str__(self):
        return self.title

class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()

class AuthorDetail(models.Model):
    tel=models.CharField(max_length=32)
    email=models.CharField(max_length=32)
    author=models.OneToOneField("Author")

class Publish(models.Model):
    name=models.CharField(max_length=32)
    email=models.CharField(max_length=32)
    def __str__(self):
        return self.name

# #收到创建第三张表
# class Author2Book(models.Model):
#     author=models.ForeignKey(to="Author")
#     book=models.ForeignKey(to="Book")

