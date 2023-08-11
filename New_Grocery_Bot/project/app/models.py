from django.db import models

# Create your models here.
class Product(models.Model):
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"barcode: {self.barcode}\n name: {self.name}"
    
