from itertools import product
from django.db import models


# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    surname=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    phone=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Outdoor','Outdoor')
    )
    name=models.CharField(max_length=100,null=True)
    price=models.FloatField()
    category=models.CharField(max_length=255,null=True,choices=CATEGORY)
    description=models.CharField(max_length=255,null=True,blank=True)
    tags=models.ManyToManyField(Tag)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS=(
        ('Delivered','Delivered'),
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery')
    )
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    note=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=100,null=True,choices=STATUS)

    def __str__(self):
        return self.product.name

    




   