from django.urls import path, include
from .views import AuthorsViewSet

from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'', AuthorsViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
