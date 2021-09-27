from django.contrib import admin

# Register your models here.
from .models import ChatRoomRecordManager as CRM

admin.site.register(CRM)