from typing import Collection
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name =  models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

class Brand(models.Model):
    name =  models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name =  models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    isDigital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()
    

    def __str__(self):
        return self.name
    
class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_line")
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field="product", blank=True)

    objects = ActiveQueryset.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order ==obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.sku)

class ProductImage(models.Model):
    alternative_text =  models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    productline = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name="product_image")
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order ==obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.url)

