from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=30)

    def get_absolute_url(self):
        return '/users/list'
    
    def __str__(self):
        return self.first_name + " " + self.last_name