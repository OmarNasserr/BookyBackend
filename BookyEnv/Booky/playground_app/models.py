from email.policy import default
from enum import unique
from tokenize import blank_re
from xmlrpc.client import DateTime
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from datetime import datetime
from django.contrib.auth.models import User
import os
from location_app.models import City
from location_app.models import Governorate


class Playground(models.Model):
    p_name = models.CharField(max_length=255)
    open_time = models.CharField(null=False, max_length=100, blank=True)
    close_time = models.CharField(null=False, max_length=100, blank=True)
    total_available_time = models.CharField(
        null=True, max_length=100, blank=True)
    description = models.CharField(
        validators=[MinLengthValidator(10)], max_length=1000)
    price_per_hour = models.FloatField(
        validators=[MinValueValidator(10)], blank=True)
    created_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)
    updated_at = models.CharField(default=str(datetime.now().strftime(
        "%d %b, %Y - %Ih%Mm%S %p")), max_length=100)

    location = models.CharField(null=True, max_length=1000, blank=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE,
                             related_name='playgrounds', to_field='city_name', blank=True)

    playground_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playground_owner',
                                         to_field='username', blank=True)

    def __str__(self):
        return self.p_name

    def calc_total_av_time(self):
        FMT = '%H:%M:%S'
        result = datetime.strptime(
            self.close_time, FMT) - datetime.strptime(self.open_time, FMT)
        return str(result)

    def save(self, *args, **kwargs):
        self.total_available_time = self.calc_total_av_time()
        self.updated_at = str(datetime.now().strftime("%d %b, %Y - %Ih%Mm%S %p"))
        super(Playground, self).save(*args, **kwargs)


def product_image_location(instance, filename):
    print("INSTANCE ", instance)
    upload_path = f"playground/{instance.playground.city.city_name}/{instance.playground.p_name}/"
    return os.path.join(upload_path, filename)


class PlaygroundImage(models.Model):
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE,
                                   related_name='images', to_field='id')
    image = models.ImageField(
        upload_to=product_image_location, blank=True, null=True, )

    thumbnail = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.playground.p_name)
