from django.urls import path
from . import views

urlpatterns = [
    path("", views.room_list_view, name="room_list"),
    path("room/<int:room_id>/", views.room_detail_view, name="room_detail"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
