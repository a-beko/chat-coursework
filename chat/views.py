from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Пароли не совпадают")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь уже существует")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect("room_list")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("room_list")
        else:
            messages.error(request, "Неверные данные")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def room_list_view(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not ChatRoom.objects.filter(name=room_name).exists():
            ChatRoom.objects.create(name=room_name)
            messages.success(request, f'Комната "{room_name}" создана')
        return redirect("room_list")

    rooms = ChatRoom.objects.all()
    return render(request, "room_list.html", {"rooms": rooms})


@login_required
def room_detail_view(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.method == "POST":
        message_text = request.POST.get("message_text")
        if message_text:
            Message.objects.create(room=room, author=request.user, text=message_text)
        return redirect("room_detail", room_id=room.id)

    messages_list = room.messages.all()
    return render(
        request, "room_detail.html", {"room": room, "messages": messages_list}
    )
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        room_id = self.request.query_params.get("room_id")
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset
