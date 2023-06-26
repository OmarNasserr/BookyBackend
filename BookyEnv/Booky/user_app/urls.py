import imp
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views.register import registeration_view
from .views.GET_requests import UsersList
from .views.PUT_DEL_requests import UserDetailUpdateDelete
#
import rest_framework_simplejwt.serializers
#
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView

)

urlpatterns = [
    path('api/register/', registeration_view, name='register'),
    
    #TokenObtainPairSerializer in rest_framework_simplejwt.serializers validate()'s func
    #was edited to return the user's info along with their
    #access token and refresh token
    
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #TokenBlacklistSerializer in rest_framework_simplejwt.serializers validate()'s func
    #was edited to return amessage that indicates that the token is blacklisted and the
    #user was logged out
    path('api/logout/', TokenBlacklistView.as_view(), name='logout'),
    
    path('list/', UsersList.as_view(), name='users-list'),
    path('<path:user_id>/detail/', UserDetailUpdateDelete.as_view(), name='users-detail'),
]
