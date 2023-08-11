from django.db import models

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    language_code = models.CharField(max_length=5)
    
    def __str__(self) -> str:
        return f"user_id:{self.id}\n" \
               f"username: {self.name}\n" \
               f"first_name: {self.first_name}\n" \
               f"last_name: {self.last_name}\n" \
               f"language_code: {self.language_code}\n"


class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=100)
    unix_time = models.DateTimeField()
    is_bot = models.BooleanField(default=False)
    user_id = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return f"username: {self.id}\n" \
               f"text: {self.text}\n" \
               f"unix_time: {self.unix_time}\n" \
               f"is_bot: {self.is_bot}\n" \
               f"user_id: {self.user_id}\n" 


class Product(models.Model):
    """
    TODO:
        - Validate barcode is only digits
    """
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"barcode: {self.barcode}\n" \
               f"name: {self.name}\n"
    
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
