from django.conf.urls import url, include
from rest_framework import routers
from . import api_views

router = routers.DefaultRouter()
router.register(r'game', api_views.GameViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
]
