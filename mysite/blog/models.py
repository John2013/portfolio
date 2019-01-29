import datetime

from django.db import models
from django.utils import timezone
from slugify import slugify


class Tag(models.Model):
	name = models.CharField('Тэг', max_length=255, null=False, unique=True)
	slug = models.CharField(max_length=255, null=False, unique=True)

	def __str__(self):
		return "<tag:{}>".format(self.name)

	def save(self, *args, **kwargs):
		if self._state.adding:
			if self.slug is None:
				self.slug = slugify(self.name)

		super().save(*args, **kwargs)


class Article(models.Model):
	title = models.CharField(
		'Заголовок', max_length=255, unique=True, null=False
	)
	slug = models.CharField(max_length=255, unique=True, null=False)
	body = models.TextField('Статья', null=False)
	preview = models.TextField('Превью', null=False)
	created_at = models.DateTimeField('Создана')
	pub_date = models.DateTimeField('Дата публикации')
	tags = models.ManyToManyField(Tag, )

	def __str__(self):
		return "<article:{}>".format(self.title[:30])

	def was_published_recently(self):
		now = timezone.now()
		# noinspection PyTypeChecker
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

	def save(self, *args, **kwargs):

		if self._state.adding:
			if self.created_at is None:
				self.created_at = timezone.now()

			if self.pub_date is None:
				self.pub_date = timezone.now()

			if self.slug is None:
				self.slug = slugify(self.title)

		super().save(*args, **kwargs)
