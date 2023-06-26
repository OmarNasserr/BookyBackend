from email.policy import default
from enum import unique
from django.db import models


class Governorate(models.Model):
    
    gov_name=models.CharField(max_length=50,unique=True)
    

    def __str__(self):
        return self.gov_name


class City(models.Model):
    city_name=models.CharField(max_length=50,unique=True)
    
    governorate=models.ForeignKey(Governorate,on_delete=models.CASCADE,related_name='city',to_field='gov_name')

    
    def __str__(self):
        return self.city_name
