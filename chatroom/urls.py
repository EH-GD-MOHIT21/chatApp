from django.urls import path
from .views import *

urlpatterns = [
    path('registerRoom',RoomRegister.as_view()),
    path('roomavailable',RoomExists.as_view()),
    path('registerprivateroom',PrivateRoomRegister.as_view()),
    path('privateroomavailable',PrivateRoomExists.as_view()),
    path('privatetokenvalidation',PrivateTokenValidation.as_view()),
]
