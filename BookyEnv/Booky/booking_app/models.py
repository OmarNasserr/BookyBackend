from django.db import models
from django.contrib.auth.models import User
import datetime

from playground_app.models import Playground
# Create your models here.


class Booking(models.Model):
    playground_id = models.ForeignKey(
        Playground, on_delete=models.CASCADE, related_name='booked_playground', to_field='id')
    reservationist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='booking_user_id', to_field='id')
    date = models.DateField()
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    booking_hours = models.IntegerField(blank=True, null=True)
    total_price_to_be_paid = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'playground {self.playground_id} was booked in {self.date} by {self.reservationist} for {self.booking_hours} hours from {self.start_time} to {self.end_time}'

    def save(self, *args, **kwargs):
        self.booking_hours = self.calc_booking_hours()
        self.total_price_to_be_paid = self.calc_total_price_to_be_paid()
        super(Booking, self).save(*args, **kwargs)
    
    def calc_total_price_to_be_paid(self):
        price_per_hour = self.playground_id.price_per_hour
        return price_per_hour * self.booking_hours

    def calc_booking_hours(self):
        FMT = '%H:%M:%S'
        result = datetime.datetime.strptime(
            self.end_time, FMT)-datetime.datetime.strptime(self.start_time, FMT)
        result = str(result).split(":")
        return int(result[0])
