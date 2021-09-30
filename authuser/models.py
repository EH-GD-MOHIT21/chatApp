from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from random import choice, randint


class CustomUserModel(models.Model):
    index = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=13)
    reset_pass_token = models.CharField(max_length=100,null=True,blank=True)
    two_factor_auth = models.BooleanField(default=True)
    send_at = models.DateTimeField(null=True,blank=True)
    
    @property
    def GenerateFPToken(self):
        length = randint(60,95)
        chars = [chr(i) for i in range(65,91)]
        chars+= [chr(i) for i in range(97,123)]
        chars += [str(i) for i in range(0,10)]
        token = ""
        for i in range(length):
            token += choice(chars)

        self.reset_pass_token = token
        return token

    @property
    def setSendTime(self):
        self.send_at = timezone.now()


class Temporarystorage(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    send_at = models.DateTimeField()
    f_name = models.CharField(max_length=40)
    l_name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    phoneno = models.CharField(max_length=13)
    

    @property
    def timestampnow(self):
        self.send_at = timezone.now()