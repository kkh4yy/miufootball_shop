from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(default="https://via.placeholder.com/150")
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    




    
    # opsional: stock dan brand
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
class employee(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    persona = models.TextField()
    #bikin model baru namanya Employee, fieldsnya ada 3:
    #bikin model baru namanya Employee, fieldsnya ada 3:
    #name: maksimal 255 karakter
    ##age: bilangan bulat
    #persona: text panjang ga ada batesan
