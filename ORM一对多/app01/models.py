from django.db import models

class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # publish：与当前书籍对象关联的的出版社对象
    publish=models.ForeignKey(to="Publish",to_field="id")

class Publish(models.Model):
    name=models.CharField(max_length=32)
    email=models.CharField(max_length=32)
    def __str__(self):
        return self.name






