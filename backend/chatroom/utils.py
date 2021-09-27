from .models import ChatRoomRecordManager as CRM
from django.utils import timezone




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



def is_room_name_correct(roomname):
    try:
        CRM.objects.get(chatroomcode=roomname)
        return True
    except:
        return False