from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from .models import ChatRoomRecordManager as CRM
from .utils import canCreateNewToken,is_room_name_correct
from time import sleep


class RoomRegister(APIView):
    def post(self,request):
        
        if not request.user.is_authenticated:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Please Login to continue.'})
        try:
            data = request.data
            roomtoken = data["rname"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        # a new token can be created after 7 days and the previous one gets delete.


        flag,status = canCreateNewToken(request.user)
        if not flag:
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':status})



        obj = CRM(index=request.user)
        Uniqueroomtoken = obj.generateRoomToken(roomtoken)
        obj.set_created
        obj.save()
        return Response({'status':HTTP_200_OK,'message':'success','token':Uniqueroomtoken})



class RoomExists(APIView):

    def post(self,request):
        # sleep(3)
        if not request.user.is_authenticated:
            return Response({'status':HTTP_403_FORBIDDEN,'message':'Invalid User.'})
        try:
            data = request.data
            room_name = data["rname"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        if is_room_name_correct(room_name):
            return Response({'status':HTTP_200_OK,'message':'success'})
        else:
            return Response({'status':HTTP_404_NOT_FOUND,'message':'Invalid Group Code.'})