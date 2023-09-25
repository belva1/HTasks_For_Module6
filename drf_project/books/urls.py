from django.urls import path, include
from .views import BooksViewSet

from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'', BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]