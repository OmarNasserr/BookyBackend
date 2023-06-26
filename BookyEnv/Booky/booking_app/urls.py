from urllib import request
from django.urls import path,include

from .views.POST_requests import BookingCreate
from .views.GET_requests import BookingsList
from .views.PUT_DELETE_requests import BookingDetail

urlpatterns = [
    path('<path:playground_id>/create/',BookingCreate.as_view(),name='booking-create'),
    path('list/',BookingsList.as_view(),name='bookings-list'),
    path('<path:booking_id>/details/',BookingDetail.as_view(),name='bookings-list'),
]
