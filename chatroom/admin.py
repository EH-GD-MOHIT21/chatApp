from django.contrib import admin

# Register your models here.
from .models import ChatRoomRecordManager as CRM,PrivateChatRoomRecordManager as PCRM

admin.site.register(CRM)
admin.site.register(PCRM)