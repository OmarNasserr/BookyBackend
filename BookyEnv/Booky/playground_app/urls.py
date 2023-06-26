from urllib import request
from django.urls import path,include
from playground_app.views.POST_requests import PlaygroundCreate
from playground_app.views.GET_requests import PlaygroundList,NearestPLaygrounds
from playground_app.views.PUT_DELETE_requests import PlaygroundDetail

urlpatterns = [
    path('create/',PlaygroundCreate.as_view(),name='playground-create'),
    path('list/',PlaygroundList.as_view(),name='playground-list'),
    path('list/nearest_playgrounds/',NearestPLaygrounds.as_view(),name='Nearest-playgrounds'),
    path('<path:playground_id>/detail/',PlaygroundDetail.as_view(),name='playground-detail'),
]
