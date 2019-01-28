import datetime

from django.db import models
from django.utils import timezone


class Tag(models.Model):
	name = models.CharField('Тэг', max_length=255, null=False)

	def __str__(self):
		return "<tag:{}>".format(self.name)


class Article(models.Model):
	title = models.CharField(
		'Заголовок', max_length=255, unique=True, null=False
	)
	body = models.TextField('Статья', null=False)
	created_at = models.DateTimeField('Создана')
	pub_date = models.DateTimeField('Дата публикации')
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return "<article:{}>".format(self.title[:30])

	def was_published_recently(self):
		now = timezone.now()
		# noinspection PyTypeChecker
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'
