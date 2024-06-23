from django.db import models

class product_model(models.Model):
    user = models.CharField(max_length=15,primary_key=True)
    product_1_title = models.CharField(max_length=50, null=True)
    product_1_category = models.CharField(max_length=12, null=True)
    product_1_link =  models.CharField(max_length=100, null=True)
    product_1_brand = models.CharField(max_length=20, null=True)
    product_2_title = models.CharField(max_length=50, null=True)
    product_2_category = models.CharField(max_length=12, null=True)
    product_2_link =  models.CharField(max_length=100, null=True)
    product_2_brand = models.CharField(max_length=20, null=True)
    product_3_title = models.CharField(max_length=50, null=True)
    product_3_brand = models.CharField(max_length=20, null=True)
    product_3_link =  models.CharField(max_length=100, null=True)
    product_3_category = models.CharField(max_length=12, null=True)
    product_4_title = models.CharField(max_length=50, null=True)
    product_4_category = models.CharField(max_length=12, null=True)
    product_4_link =  models.CharField(max_length=100, null=True)
    product_4_brand = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.user or ''
