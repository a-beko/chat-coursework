from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r"rooms", views.RoomViewSet)
router.register(r"messages", views.MessageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", obtain_auth_token, name="api_token_auth"),
]
