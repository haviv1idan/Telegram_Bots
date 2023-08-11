from django.db import models

# Create your models here.
class Product(models.Model):
    """
    TODO:
        - Validate barcode is only digits
    """
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"barcode: {self.barcode}\n name: {self.name}"
    
class Shop(models.Model):
    chain = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    distance = models.CharField(max_length=100)
    sale = models.CharField(max_length=100, null=True)
    price = models.FloatField(max_length=100)
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return f"chain: {self.chain}\n" \
               f"name: {self.name}\n" \
               f"address: {self.address}\n" \
               f"distance: {self.distance}\n" \
               f"sale: {self.sale}\n" \
               f"price: {self.price}\n" \
               f"barcode: {self.barcode}\n"


class OnlineShop(models.Model):
    chain = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    sale = models.CharField(max_length=100, null=True)
    price = models.FloatField(max_length=100)
    barcode = models.CharField(max_length=100)

    def __str__(self):
        return f"chain: {self.chain}\n" \
               f"name: {self.name}\n" \
               f"website: {self.website}\n" \
               f"sale: {self.sale}\n" \
               f"price: {self.price}\n" \
               f"barcode: {self.barcode}\n"
