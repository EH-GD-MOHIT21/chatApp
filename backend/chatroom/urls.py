from django.urls import path
from .views import *

urlpatterns = [
    path('registerRoom',RoomRegister.as_view()),
    path('roomavailable',RoomExists.as_view()),
]
