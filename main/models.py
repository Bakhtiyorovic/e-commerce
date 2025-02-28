from django.db import models
# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='Images/')
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

