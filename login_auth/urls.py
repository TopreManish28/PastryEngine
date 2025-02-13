from django.urls import path
from .views import RegisterView,StudentList
from login_auth import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='User Registration'),
    path('student/', StudentList.as_view()),
]
