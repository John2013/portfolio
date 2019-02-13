from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, \
	WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

	def connect(self):
		# Join room group
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)

		self.accept()

	def disconnect(self, close_code):
		# Leave room group
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	# noinspection PyMethodOverriding
	def receive(self, text_data):
		text_data_json = json.loads(text_data, encoding='utf8')
		message = text_data_json['message']
		nickname = text_data_json['nickname']
		datetime = text_data_json['datetime']

		# Send message to room group
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'nickname': nickname,
				'datetime': datetime,
			}
		)

	# Receive message from room group
	def chat_message(self, event):
		message = event['message']
		nickname = event['nickname']
		datetime = event['datetime']

		# Send message to WebSocket
		self.send(text_data=json.dumps({
			'message': message,
			'nickname': nickname,
			'datetime': datetime,
		}))


class ChatAsyncConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		print('connect')
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		print('disconnect')
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	# noinspection PyMethodOverriding
	async def receive(self, message_data):
		print('receive')
		text_data_json = json.loads(message_data, encoding='utf8')
		message = text_data_json['message']
		nickname = text_data_json['nickname']
		datetime = text_data_json['datetime']

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'nickname': nickname,
				'datetime': datetime,
			}
		)

	# Receive message from room group
	async def chat_message(self, event):
		print('chat_message')
		message = event['message']
		nickname = event['nickname']
		datetime = event['datetime']

		text_data = json.dumps({
			'message': message,
			'nickname': nickname,
			'datetime': datetime,
		},
			ensure_ascii=False,
			encoding='utf8'
		)
		print(text_data)

		# Send message to WebSocket
		await self.send(
			text_data=text_data
		)
