from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterView.as_view(), name='User Registration'),
    path('login/', LoginView.as_view(), name="User Login"),
    path('logout/', LogoutView.as_view(), name="User logout"),
]