from urllib import request
from django.urls import path,include
from location_app.views.POST_requests import CityCreate,GovCreate
from .views.GET_requests import CitiesList, GovList
from .views.PUT_requests import CityDetail,GovDetail

urlpatterns = [
    path('cities/create/',CityCreate.as_view(),name='city-create'),
    path('cities/list/',CitiesList.as_view(),name='cities-list'),
    path('cities/<path:city_id>/detail/',CityDetail.as_view(),name='city-detail'),
    path('gov/create/',GovCreate.as_view(),name='gov-create'),
    path('gov/list/',GovList.as_view(),name='gov-list'),
    path('gov/<path:gov_id>/detail/',GovDetail.as_view(),name='gov-detail'),
]
