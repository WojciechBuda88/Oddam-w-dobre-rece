from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField(null=False)
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=False)
    phone_number = models.IntegerField(null=False)
    city = models.CharField(max_length=128, null=False)
    pick_up_date = models.DateField(null=False)
    pick_up_time = models.TimeField(null=False)
    pick_up_comment = models.TextField(null=True)


class Institution(models.Model):
    INSTITUTIONS = (
        ('Fundacja', 'Fundacja'),
        ('Organizacja pozarządowa', 'Organizacja pozarządowa'),
        ('Zbiórka lokalna', 'Zbiórka lokalna'),
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=25, choices=INSTITUTIONS, default='Fundacja')
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.name
