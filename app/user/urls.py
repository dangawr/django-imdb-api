from rest_framework.authtoken.views import obtain_auth_token
from .views import logout_view, RegisterUserApiView, UpdateUserView
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('token/', obtain_auth_token, name='token'),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('me/', UpdateUserView.as_view(), name='me'),
]
