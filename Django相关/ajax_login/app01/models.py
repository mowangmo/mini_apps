from django.db import models

class User(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=62)

    def __str__(self):
        return self.user