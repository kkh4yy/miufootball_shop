from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(default="https://via.placeholder.com/150")
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    
    # opsional: stock dan brand
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name