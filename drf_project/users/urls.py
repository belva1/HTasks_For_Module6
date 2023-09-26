from django.urls import path
from .views import UserDetail

urlpatterns = [
    path('user-detail/', UserDetail.as_view(), name='user-detail'),
]