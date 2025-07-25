from django.db import models
# built in user model
from django.contrib.auth.models import User

class Product(models.Model):

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    image_url = models.URLField(max_length=200)
    description = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name







