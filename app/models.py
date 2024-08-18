from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser

# Create your models here.
class Flower(models.Model):
    CAT=((1,'RedRose'),(2,'YelloRose'),(3,'WhiteRose'),(4,'PinkRose'),(5,'Flower'),(6,'Combos'),(7,'Birthday'),(8,'Anniversary'),(9,'Plants'),(10,'Personalised'),(11,'Occasions'),(12,'Chocolate_Bouquet'),(13,'Special'))
    fname=models.CharField(max_length=50,verbose_name='Bouquet Name')
    price=models.IntegerField(verbose_name='Price')
    is_active=models.BooleanField(default=True)
    fimage=models.ImageField(upload_to='image')
    cat=models.IntegerField(choices=CAT,verbose_name='Category')
    flowert=models.CharField(max_length=70,verbose_name='Flower Type')
    nos=models.IntegerField(verbose_name='No. Of Stems')
    flowc=models.CharField(max_length=100,verbose_name='Flower Contains')
    packing=models.CharField(max_length=70,verbose_name='Packing')
    packingc=models.CharField(max_length=70,verbose_name='Packing Color')
    ribb=models.CharField(max_length=70,verbose_name='Ribbons')
    np=models.CharField(max_length=70,verbose_name='No. Of Packing')

class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Flower',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)    



class Order(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Flower',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)  
    amt=models.IntegerField()   

class Udetail(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    society=models.CharField(max_length=200)
    area=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    pho=models.IntegerField(max_length=10)
    uname=models.CharField(max_length=50)

class History(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey('Flower',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)  
    amt=models.IntegerField() 

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=50)
    contact=models.IntegerField()
    Message=models.CharField(max_length=200)    
    
