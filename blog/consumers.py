from channels.generic.websocket import AsyncWebsocketConsumer
import json

from blog.models import Comment, Article


class ChatConsumer(AsyncWebsocketConsumer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

	async def connect(self):
		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	# noinspection PyMethodOverriding
	async def receive(self, text_data):
		text_data_json = json.loads(text_data, encoding='utf8')
		message = text_data_json['message']
		nickname = text_data_json['nickname']
		datetime = text_data_json['datetime']
		article_pk = text_data_json['articlePk']

		comment = Comment(
			article_id=article_pk,
			body=message,
			nickname=nickname,
			datetime=datetime
		)
		comment.save()

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
