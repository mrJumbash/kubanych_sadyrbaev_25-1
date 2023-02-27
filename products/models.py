from django.db import models


class Hashtag(models.Model):
    title = models.CharField(max_length=55)

    def __str__(self):
        return self.title


class Product(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    quantity = models.IntegerField(null=True)
    price = models.FloatField(default=0.0)
    hashtags = models.ManyToManyField(Hashtag)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.CharField(max_length=255)
    rate = models.FloatField(default=0.0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)