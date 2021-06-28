from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    locationX = models.FloatField(default=0)
    locationY = models.FloatField(default=0)
    isFarmer = models.BooleanField(default=False)
    farmerPicture = models.ImageField(null=True, blank=True, default="/placeholder.png")
    farmPicture = models.ImageField(null=True, blank=True, default="/placeholder.png")
    farmName = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    farmerPoint = models.FloatField(default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    deposit = models.FloatField(default=0)
    

class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default="/placeholder.png")
    description = models.TextField(null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    category = models.CharField(max_length=200, null=True, blank=True)
    unitPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )

    productPoint = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    productionTime = models.DateTimeField(null=True,blank=True)
    distance = models.FloatField(default=0)
    
    def __str__(self):
        return self.name





class Review(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    productPoint = models.IntegerField(null=True, blank=True, default=0)
    deliveryPoint = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)


class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    orderqr = models.ImageField(null=True, blank=True, default="/placeholder.png")

    def __str__(self):
        return str(self.createdAt)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    isBoxDelivery = models.BooleanField(default=False)

    def __str__(self):
        return str(self.address)


class ShipmentCompany(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    info = models.TextField(null=True, blank=True)


class DirectDelivery(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    shippingAddress = models.OneToOneField(
        ShippingAddress, on_delete=models.CASCADE, null=True, blank=True
    )
    shipmentCompany = models.ForeignKey(
        ShipmentCompany, on_delete=models.SET_NULL, null=True
    )


class Box(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    locationX = models.FloatField(default=0)
    locationY = models.FloatField(default=0)
    status = models.CharField(max_length=200, null=True, blank=True)
    temperature = models.FloatField(default=0)
    key = models.IntegerField(null=True, blank=True, default=0)


class BoxDelivery(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    shippingAddress = models.OneToOneField(
        ShippingAddress, on_delete=models.CASCADE, null=True, blank=True
    )
    shipmentCompany = models.ForeignKey(
        ShipmentCompany, on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)
