from django.db import models

# Create your models here.
class Product(models.Model):
    proudct_id=models.AutoField
    product_name= models.CharField(max_length=50)
    category=models.CharField(max_length=50, default="")
    subcategory=models.CharField(max_length=50, default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=1000)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    cel = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    textarea = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Orders(models.Model):
     itemsJson=models.CharField(max_length=5000,default="")
     order_id= models.AutoField(primary_key=True)
     amount= models.IntegerField(default=0)
     name=models.CharField(max_length=50)
     email=models.CharField(max_length=50)
     address=models.CharField(max_length=500)
     phone=models.CharField(max_length=50)
     state=models.CharField(max_length=50)
     city=models.CharField(max_length=50)
     zip_code=models.CharField(max_length=50)

class orderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7]+"..."