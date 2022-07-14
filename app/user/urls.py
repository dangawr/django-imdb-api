from rest_framework.authtoken.views import obtain_auth_token
from .views import register_view, logout_view
from django.urls import path

urlpatterns = [
    path('token/', obtain_auth_token, name='token'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]
