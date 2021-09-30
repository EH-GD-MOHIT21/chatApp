from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from .models import ChatRoomRecordManager as CRM,PrivateChatRoomRecordManager as PCRM
from .utils import canCreateNewToken,is_room_name_correct,canCreateNewPrivateToken,Is_Valid_Private_Room,Generate_key,Decode_Key,IsStrongPassword
from django.contrib.auth.hashers import make_password
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


class PrivateRoomRegister(APIView):
    def post(self,request):
        
        if not request.user.is_authenticated:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Please Login to continue.'})
        try:
            data = request.data
            roomtoken = data["rname"]
            password = data["password"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        # a new token can be created after 7 days and the previous one gets delete.


        flag,status = canCreateNewPrivateToken(request.user)
        if not flag:
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':status})

        # password validation here

        if not IsStrongPassword(password):
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':'Please use digits chars special chars as password minimum length 8.'})

        obj = PCRM(index=request.user)
        Uniqueroomtoken = obj.generateRoomToken(roomtoken)
        obj.set_created
        obj.password = make_password(password)
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

            

class PrivateRoomExists(APIView):
    def post(self,request):
        # sleep(3)
        if not request.user.is_authenticated:
            return Response({'status':HTTP_403_FORBIDDEN,'message':'Invalid User.'})
        try:
            data = request.data
            room_name = data["rname"]
            password = data["password"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})

        if Is_Valid_Private_Room(room_name,password):
            response = Response({'status':HTTP_200_OK,'message':'success'})
            if 'chattoken' in request.COOKIES:
                value = request.COOKIES['chattoken']
            else:
                response.set_cookie('chattoken', Generate_key(room_name,password))
            return response
        else:
            return Response({'status':HTTP_404_NOT_FOUND,'message':'Invalid Group Code or password'})



class PrivateTokenValidation(APIView):
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({'status':HTTP_403_FORBIDDEN,'message':'Invalid User.'})
        try:
            data = request.data
            room_name = data["rname"]
            token = data["rtoken"][2:-1]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})

        is_valid = Decode_Key(token)
        if is_valid:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'success'})
        return Response({'status':HTTP_403_FORBIDDEN,'message':'USER NOT FOUND or Invalid Group Credentials.'})