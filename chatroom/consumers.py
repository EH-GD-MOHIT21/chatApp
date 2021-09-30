import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoomRecordManager as CRM,PrivateChatRoomRecordManager as PCRM
from .utils import Decode_Key

class ChatConsumer(AsyncWebsocketConsumer):

    def usermanager(self):
        try:
            obj = CRM.objects.get(chatroomcode=self.room_name)
            obj.active_members += 1
            obj.save()
        except Exception as e:
            pass

    def removeactive(self):
        try:
            obj = CRM.objects.get(chatroomcode=self.room_name)
            obj.active_members -= 1
            obj.save()
        except Exception as e:
            pass

    def getActiveMembers(self):
        try:
            obj = CRM.objects.get(chatroomcode=self.room_name)
            return obj.active_members
        except:
            return None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if not self.scope["user"].is_authenticated:
            self.close()

        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()

            await sync_to_async(self.usermanager,thread_sensitive=True)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': str(self.scope["user"].first_name) + " " + str(self.scope["user"].last_name) + " " + str(self.scope["user"]) + " joined the group.",
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'ext':True,
                    'number_of_users':  await sync_to_async(self.getActiveMembers,thread_sensitive=True)()
                }
            )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_authenticated:
            await sync_to_async(self.removeactive,thread_sensitive=True)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': str(self.scope["user"].first_name) + " " + str(self.scope["user"].last_name) + " " + str(self.scope["user"]) + " left the group.",
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'ext':True,
                    'number_of_users':  await sync_to_async(self.getActiveMembers,thread_sensitive=True)()
                }
            )
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        if self.scope["user"].is_authenticated:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'username': self.scope["user"].username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        if self.scope["user"].is_authenticated:
            message = event['message']

            # prevention from xss
            lower_msg = message.lower()
            if 'script' in lower_msg:
                message = 'Message Not Available.'

            try:
                is_ext = event['ext']
            except:
                is_ext = False

            try:
                user = event["user"]
            except:
                user = self.scope["user"].first_name + " " + self.scope["user"].last_name

            try:
                username = event["username"]
            except:
                username = self.scope["user"].username

            try:
                number_of_users = event["number_of_users"]
            except:
                number_of_users = await sync_to_async(self.getActiveMembers,thread_sensitive=True)()

            
            await self.send(text_data=json.dumps({
                'message': message,
                'user': user,
                'ext':is_ext,
                'username':username,
                "number_of_users":number_of_users
            }))


# to be checked
class PrivateChatConsumer(AsyncWebsocketConsumer):

    def usermanager(self):
        try:
            obj = PCRM.objects.get(chatroomcode=self.room_name)
            obj.active_members += 1
            obj.save()
        except Exception as e:
            print(e)
            pass

    def removeactive(self):
        try:
            obj = PCRM.objects.get(chatroomcode=self.room_name)
            obj.active_members -= 1
            obj.save()
        except Exception as e:
            # print(e)
            pass

    def getActiveMembers(self):
        try:
            obj = PCRM.objects.get(chatroomcode=self.room_name)
            return obj.active_members
        except Exception as e:
            # print(e)
            return None

    async def connect(self):
        flag = 0
        token = None
        for element in self.scope["headers"]:
            if element[0] == b'cookie':
                try:
                    token = str(element[1])[2:-1].split('chattoken=')[1][4:-3]
                except:
                    self.close()
                flag = 1
                break
        if not flag:
            self.close()
        try:
            if not Decode_Key(token):
                self.close()
        except:
            self.close()
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if not self.scope["user"].is_authenticated:
            self.close()

        elif token == None:
            self.close()

        else:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )

            await self.accept()

            await sync_to_async(self.usermanager,thread_sensitive=True)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': str(self.scope["user"].first_name) + " " + str(self.scope["user"].last_name) + " " + str(self.scope["user"]) + " joined the group.",
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'ext':True,
                    'number_of_users':  await sync_to_async(self.getActiveMembers,thread_sensitive=True)()
                }
            )


    async def disconnect(self, close_code):
        # Leave room group

        flag = 0
        token = None
        for element in self.scope["headers"]:
            if element[0] == b'cookie':
                try:
                    token = str(element[1])[2:-1].split('chattoken=')[1][4:-3]
                except:
                    self.close()
                flag = 1
                break
        if not flag:
            self.close()
        try:
            if not Decode_Key(token):
                self.close()
        except:
            self.close()


        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_authenticated and token!=None:
            await sync_to_async(self.removeactive,thread_sensitive=True)()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': str(self.scope["user"].first_name) + " " + str(self.scope["user"].last_name) + " " + str(self.scope["user"]) + " left the group.",
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'ext':True,
                    'number_of_users':  await sync_to_async(self.getActiveMembers,thread_sensitive=True)()
                }
            )
        

    # Receive message from WebSocket
    async def receive(self, text_data):

        flag = 0
        token = None
        for element in self.scope["headers"]:
            if element[0] == b'cookie':
                try:
                    token = str(element[1])[2:-1].split('chattoken=')[1][4:-3]
                except:
                    self.close()
                flag = 1
                break

        if not flag:
            self.close()

        try:
            if not Decode_Key(token):
                self.close()
        except:
            self.close()

        if token == None:
            self.close()

        elif self.scope["user"].is_authenticated:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.scope["user"].first_name + " " + self.scope["user"].last_name,
                    'username': self.scope["user"].username
                }
            )

    # Receive message from room group
    async def chat_message(self, event):

        if self.scope["user"].is_authenticated:
            message = event['message']

            # prevention from xss
            lower_msg = message.lower()
            if 'script' in lower_msg:
                message = 'Message Not Available.'

            try:
                is_ext = event['ext']
            except:
                is_ext = False

            try:
                user = event["user"]
            except:
                user = self.scope["user"].first_name + " " + self.scope["user"].last_name

            try:
                username = event["username"]
            except:
                username = self.scope["user"].username

            try:
                number_of_users = event["number_of_users"]
            except:
                number_of_users = await sync_to_async(self.getActiveMembers,thread_sensitive=True)()

            
            await self.send(text_data=json.dumps({
                'message': message,
                'user': user,
                'ext':is_ext,
                'username':username,
                "number_of_users":number_of_users
            }))

