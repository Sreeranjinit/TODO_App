from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    Name=models.CharField(max_length=20)
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    Complete=models.BooleanField(default=False)
    Date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Name
    

