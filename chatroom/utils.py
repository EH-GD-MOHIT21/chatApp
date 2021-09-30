from .models import ChatRoomRecordManager as CRM,PrivateChatRoomRecordManager as PCRM
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.conf import settings
from cryptography.fernet import Fernet


def canCreateNewToken(user):
    try:
        crm = CRM.objects.get(index=user)
        timeCreated = crm.created_at
        timeNow = timezone.now()
        del_time = timeNow - timeCreated
        if int(del_time.days) < 7:
            return (False,"You can create new token after 7 days.")
        else:
            crm.delete()
            return (True,None)
    except:
        return (True,None)


def canCreateNewPrivateToken(user):
    try:
        crm = PCRM.objects.get(index=user)
        timeCreated = crm.created_at
        timeNow = timezone.now()
        del_time = timeNow - timeCreated
        if int(del_time.days) < 7:
            return (False,"You can create new token after 7 days.")
        else:
            crm.delete()
            return (True,None)
    except:
        return (True,None)



def is_room_name_correct(roomname):
    try:
        CRM.objects.get(chatroomcode=roomname)
        return True
    except:
        return False


def Is_Valid_Private_Room(roomname,raw_pass):
    try:
        password = PCRM.objects.get(chatroomcode=roomname).password
        if check_password(raw_pass,password):
            return True
        return False
    except:
        return False


def Generate_key(group,password):
    data = (group+"<%m$?%^#>"+password)
    a = Fernet(settings.COOKIE_KEY)
    coded_slogan = a.encrypt(data.encode())
    return coded_slogan

def Decode_Key(coded_slogan):
    try:
        b = Fernet(settings.COOKIE_KEY)
        decoded_slogan = str(b.decrypt(bytes(coded_slogan,'UTF-8'))).split('<%m$?%^#>')
        room_name = decoded_slogan[0][2:]
        password = decoded_slogan[1][:-1]
        if Is_Valid_Private_Room(room_name,password):
            return True
        return False
    except:
        return False


def IsStrongPassword(password):
    if password.isalnum() or password.isalpha() or password.isnumeric() or password.isspace() or len(password)<8:
        return False
    return True