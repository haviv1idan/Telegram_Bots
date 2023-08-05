from django.db import models


# Create your models here.
class Product(models.Model):
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"barcode: {self.barcode}, name: {self.name}"


class Shop(models.Model):
    chain = models.TextField()
    name = models.TextField()
    address = models.TextField()
    distance = models.TextField()
    sale = models.TextField(null=True)
    price = models.TextField()
    barcode = models.TextField()

    def __str__(self):
        return f"chain: {self.chain}\n" \
               f"name: {self.name}\n" \
               f"address: {self.address}\n" \
               f"distance: {self.distance}\n" \
               f"sale: {self.sale}\n" \
               f"price: {self.price}\n" \
               f"barcode: {self.barcode}\n"
