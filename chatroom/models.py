from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoomRecordManager(models.Model):
    index = models.ForeignKey(User,on_delete=models.CASCADE)
    chatroomcode = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(null=True,blank=True)
    active_members = models.IntegerField(default=0)
    
    def generateRoomToken(self,name):
        time = str(timezone.now())
        exceptions = [' ','-',':','.','+']

        for i in exceptions:
            time = time.replace(i,'_')

        self.chatroomcode = str(name)+str(time)
        return self.chatroomcode


    @property
    def set_created(self):
        self.created_at = timezone.now()


class PrivateChatRoomRecordManager(models.Model):
    index = models.ForeignKey(User,on_delete=models.CASCADE)
    chatroomcode = models.CharField(max_length=100,unique=True)
    created_at = models.DateTimeField(null=True,blank=True)
    active_members = models.IntegerField(default=0)
    is_private = models.BooleanField(default=True)
    password = models.TextField()

    def generateRoomToken(self,name):
        time = str(timezone.now())
        exceptions = [' ','-',':','.','+']

        for i in exceptions:
            time = time.replace(i,'_')

        self.chatroomcode = str(name)+str(time)
        return self.chatroomcode

    @property
    def set_created(self):
        self.created_at = timezone.now()