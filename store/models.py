from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    product_price = models.FloatField(max_length=6)
    target_price = models.FloatField(max_length=6)
    product_image = models.URLField(max_length=512)
    product_url = models.URLField(max_length=2000, unique=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
