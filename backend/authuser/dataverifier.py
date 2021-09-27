import smtplib
from email.message import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from random import randint

from rest_framework.response import Response
from .models import Temporarystorage as TPS,User,CustomUserModel as cum
from django.utils import timezone
from django.contrib.auth import login,authenticate,logout


def phoneverifier(phone):
    if len(phone)!=10 or not(phone.isnumeric()):
        return False
    return True


def verifyname(name):
    if len(name) < 3:
        return False
    
    if not name.isalpha():
        return False
    return True

def preprocessmail(mail):
    if mail.count('@')!=1:
        return False
    if len(mail)<5:
        return False
    try:
        User.objects.get(email=mail)
        return False
    except:
        pass
    
    try:
        # deleting all previous records that doesnot register successfully.
        TPS.objects.filter(send_at__lt=timezone.now()-timezone.timedelta(minutes=5)).delete()
    except:
        pass

    try:
        obj = TPS.objects.get(email=mail)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            return False
        if int(minutes)<=5:
            return True
        return False
    except:
        return False


def passwordManager(p1,p2):
    if len(p1)<8:
        return False
    if p1!=p2:
        return False
    if p1.isnumeric() or p1.isalpha() or p1.isalnum():
        return False
    return True


def otpmatch(original,submitted):
    return original==submitted




def isvalidemail(mail):
    if mail.count('@')!=1:
        return False
    if len(mail)<5:
        return False
    try:
        User.objects.get(email=mail)
        return False
    except:
        pass
    return True

@csrf_exempt
def sendmail(request=None,to=None,subject=None,messageper=None,otp=None):
    message = EmailMessage()
    ## deleting temporary storage objects that have Expired.
    try:
        # deleting all previous records that doesnot register successfully.
        TPS.objects.filter(send_at__lt=timezone.now()-timezone.timedelta(minutes=5)).delete()
    except:
        pass

    if to!=None:
        message['To'] = to
    else:
        email_l = json.loads(request.body).get('email')
        if not isvalidemail(email_l):
            return JsonResponse({'result':'Invalid Mail Id.'})
        message['To'] = email_l
    if subject!=None:
        message['Subject'] = subject
    else:
        message['Subject'] = "Welcome to ChatApp.com"
    message['From'] = settings.EMAIL_SENDER
    if messageper==None:
        message.set_content(f"Hello User welcome to ChatApp.com Your one time password is {otp} valid for 5 minutes.\n\n\n Happy Chatting.\n Regards\n ChatApp.com")
    else:
        message.set_content(messageper)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_SENDER, settings.PASS_SENDER)
        server.send_message(message)
        if to==None:
            store_at = TPS(email=email_l,otp=otp)
            store_at.timestampnow
            store_at.save()
            return JsonResponse({'result':'Success'})
        else:
            return 'success'
    except Exception as e:
        print(e)
        if to==None:
            return JsonResponse({'result': 'Email Not Send. Server Error..'})
        else:
            return 'Email Not send.'

def randomotpgen():
    return randint(100000,999999)

def islimitdone(email):
    try:
        User.objects.get(email=email)
        return (False,"Mail id Already Exists")
    except Exception as e:
        # print(e)
        pass
    try:
        obj = TPS.objects.get(email=email)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            obj.delete()
            return (True,None)
        if int(minutes)>=5:
            obj.delete()
            # delete record
            return (True,None)
        return (False,'Otp has been send please try again 5 minutes.')
    except:
        return (True,None)



def CreateCumDeleteTS(email):
    umodel = User()
    
    _ = TPS.objects.get(email=email)
    umodel.first_name = _.f_name
    umodel.last_name = _.l_name
    umodel.username = email
    umodel.email = email
    umodel.set_password(_.password)
    umodel.save()

    model = cum(index=umodel)
    model.phone_no = _.phoneno

    model.save()


def otp_match(otp,email):
    try:
        obj = TPS.objects.get(email=email)
        if str(otp)!= str(obj.otp):
            return False
        else:
            # save data here to permanent model
            CreateCumDeleteTS(email)
            obj.delete()
            return True
    except:
        return False



def createTpsStorage(data):
    # create a temporary object with otp and returns otp
    model = TPS()
    model.f_name = data["fname"]
    model.l_name = data["lname"]
    model.email = data["email"]
    model.password = data["password"]
    model.phoneno = data["phoneno"]

    model.timestampnow

    otp = randomotpgen()
    model.otp = otp

    model.save()

    return otp


def logoutmanager(request):
    logout(request)


def loginmanager(request,username,password):
    user = authenticate(request,username=username,password=password)
    if user is None:
        return user
    login(request,user)
    return user


def istokenexpired(email):
    try:
        print('hmmm')
        user = User.objects.get(username=email)
        token = cum.objects.get(index=user).reset_pass_token
        if token == '' or token == None:
            return True
        else:
            timesend = cum.objects.get(index=user).send_at
            timenow = timezone.now()
            del_time = timenow - timesend
            hours,minutes,seconds = map(float,del_time.split(':'))
            print(hours,minutes,seconds)
            if int(hours)!=0:
                return (True)
            if int(minutes)>=5:
                # delete record
                return (True)
            return (False)
    except Exception as e:
        print(e)
        return False


def valid_check_FP(email):
    try:
        umodel = User.objects.get(email=email)
        cmodel = cum.objects.get(index=umodel)
    except:
        return (False,"Can't find user.")
    try:
        if cmodel.reset_pass_token == '' or cmodel.reset_pass_token == None or istokenexpired(email):
            token = cmodel.GenerateFPToken
            url = settings.BASE_URL + f"validate/user={email}/token={cmodel.reset_pass_token}"
            ## send mail here 
            res = sendmail(to=email,otp=url,subject="This mail is send for your password Recovery on ChatApp.com",messageper=f"Your Token For Password Recovry is \n \n \n {url} \n \n \n Thanks \n Regards \n ChatApp.com ")
            if res == 'success':
                cmodel.setSendTime
                cmodel.save()
                return (True,"Token Send")
            else:
                return (False,"Server Error Email Not Send.")
        else:
            return (False,"Token Already Send")
    except:
        return (False,"Server Error Mail Can't be send")



def ResetTokenAndMailVerified(email,token):
    try:
        user = User.objects.get(email=email)
        cumuser = cum.objects.get(index=user)
        if cumuser.reset_pass_token != token:
            return False
    except:
        return False
    return True



def checkTimeLimitFP(email):
    try:
        user = User.objects.get(email=email)
        obj = cum.objects.get(index=user)
        send_time = obj.send_at
        cur_time = timezone.now()
        del_time = str(cur_time-send_time)
        hours,minutes,seconds = map(float,del_time.split(':'))
        if int(hours)!=0:
            obj.send_at = None
            obj.reset_pass_token = None
            obj.save()
            return (True,None)
        if int(minutes)>=5:
            obj.send_at = None
            obj.reset_pass_token = None
            obj.save()
            return (True,None)
        return (False,'Token has been send please try again 5 minutes.')
    except:
        return (True,None)


def changePasswordForToken(email,token,password):
    try:
        user = User.objects.get(email=email)
        cumuser = cum.objects.get(index=user)
        if cumuser.reset_pass_token != token:
            return False
        user.set_password(password)
        cumuser.send_at = None
        cumuser.reset_pass_token = None
        user.save()
        cumuser.save()
        #### notify user that password has been changed
        res = sendmail(to=email,messageper=f"Hello {user.first_name} {user.last_name} . Your Password Has Been Successfully Changed On ChatApp.com \n \n Thanks \n Regards \n ChatApp.com ",subject="Password Changed On ChatApp.com")
        return True
    except:
        return False