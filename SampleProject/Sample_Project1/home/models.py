from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    enrolled_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    img=models.ImageField(upload_to='pics')
    
    #Remigration example
    mark = models.IntegerField(default=0)
