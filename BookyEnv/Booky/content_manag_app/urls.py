from urllib import request
from django.urls import path,include
from .homepage.views.POST_requests import SliderImageCreate
from .homepage.views.GET_requests import SliderImageList
from .homepage.views.PUT_DEL_requests import SliderImageDetail

urlpatterns = [
    path('create/',SliderImageCreate.as_view(),name='slider-image-create'),
    path('list/',SliderImageList.as_view(),name='slider-image-list'),
    path('<path:slider_image_id>/detail/',SliderImageDetail.as_view(),name='slider-image-detail'),
]
