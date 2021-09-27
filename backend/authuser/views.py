from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from .dataverifier import *

# Create your views here.

class register(APIView):
    def post(self,request):

        data = request.data
        if data == None:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request'})

        try:
            name_f = data["fname"]
            name_l = data["lname"]
            email_r = data["email"]
            pass_r = data["password"]
            cpass_r = data["cpassword"]
            phone_r = data["phoneno"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})

        if not verifyname(name_f) or not verifyname(name_l):
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':'Invalid Entry for name.'})
        
        if not passwordManager(pass_r,cpass_r):
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':'Please use strong password chars,nums,special chars and both password fields should be match.'})
        
        if not isvalidemail(email_r):
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':'Invalid Mail or It already Taken.'})

        if not phoneverifier(phone_r):
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':'Invalid Phone Number.'})

        state,message = islimitdone(email_r)
        if state:
            otp = createTpsStorage(data)
            sendmail(to=email_r,otp=otp,)
            return Response({'status':HTTP_200_OK,'message':'otp send on mailid.'})
        else:
            return Response({'status':HTTP_408_REQUEST_TIMEOUT,'message':message})

        


class verifyuserregister(APIView):
    def post(self,request):
        data = request.data
        try:
            data["otp"]
            data["email"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        if not islimitdone(data["email"])[0] and islimitdone(data["email"])[1]!='Mail id Already Exists' and otp_match(data["otp"],data["email"]):
            return Response({'status':HTTP_200_OK,'message':'success'})
        return Response({'status':HTTP_404_NOT_FOUND,'message':'Invalid OTP. if OTP expired please refresh page to sign up Again.'})


class logoutuser(APIView):
    def post(self,request):
        logoutmanager(request)

        return Response({'status':HTTP_200_OK,'message':'successfully logged out.'})

    def get(self,request):
        logoutmanager(request)

        return Response({'status':HTTP_200_OK,'message':'successfully logged out.'})


class logginuser(APIView):
    def post(self,request):
        try:
            data = request.data
            username = data["username"]
            password = data["password"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':';Invalid Request.'})
        user = loginmanager(request,username,password)
        if user is None:
            return Response({'status':HTTP_404_NOT_FOUND,'message':'Invalid Username or Password'})
        return Response({'status':HTTP_200_OK,'message':'success'})


class ForgotPassGen(APIView):
    def post(self,request):
        try:
            email = request.data["email"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        res = checkTimeLimitFP(email)
        if not res[0]:
            return Response({'status':HTTP_406_NOT_ACCEPTABLE,'message':res[1]})
        check = valid_check_FP(email)
        if check[0]:
            return Response({'status':HTTP_200_OK,'message':'Recovery Option Send on mail.'})
        else:
            return Response({'status':HTTP_404_NOT_FOUND,'message':check[1]})


class VerifyUserTokenAndUpdate(APIView):
    def post(self,request,email=None,token=None):
        # print(request.headers)
        if email == None or token == None:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        if not ResetTokenAndMailVerified(email,token):
            return Response({'status':HTTP_401_UNAUTHORIZED,'message':'Invalid Request.'})
        data = request.data
        try:
            password = data["password"]
            cpassword = data["cpassword"]
        except:
            return Response({'status':HTTP_400_BAD_REQUEST,'message':'Invalid Request.'})
        if password != cpassword:
            return Response({'status':HTTP_203_NON_AUTHORITATIVE_INFORMATION,'message':'Both Password Does not match.'})
        if passwordManager(password,cpassword):
            res = checkTimeLimitFP(email)
            if not res[0]:
                if changePasswordForToken(email,token,password):
                    return Response({'status':HTTP_200_OK,'message':'Success'})
                else:
                    return Response({'status':HTTP_500_INTERNAL_SERVER_ERROR,'message':'something went wrong.'})
            else:
                return Response({'status':HTTP_400_BAD_REQUEST,'message':'Time Limit Excceed Session Expired Please Try Again.'})
        else:
            return Response({'status':HTTP_203_NON_AUTHORITATIVE_INFORMATION,'message':'please use minimum 8 characters/digits special letters as password.'})



class is_user_auth(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            return Response({'status':HTTP_200_OK,'message':True})
        return Response({'status':HTTP_200_OK,'message':False})


class GetUsername(APIView):
    def get(self,request):
        if request.user.is_authenticated:
            return Response({'status':HTTP_200_OK,'message':request.user.username,'name':request.user.first_name + " " + request.user.last_name})
        return Response({'status':HTTP_401_UNAUTHORIZED,'message':'Invalid Request.'})