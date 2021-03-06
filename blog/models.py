import datetime

from django.db import models
from django.utils import timezone
from slugify import slugify


class Tag(models.Model):
	name = models.CharField('Тэг', max_length=255, null=False, unique=True)
	slug = models.SlugField(unique=True, blank=True, null=False)

	class Meta:
		verbose_name = "Тег"
		verbose_name_plural = "Теги"

	def __str__(self):
		return self.name

	def _get_unique_slug(self):
		slug_max_size = 50
		slug = slugify(self.name)[:slug_max_size]
		unique_slug = slug
		num = 1

		while Tag.objects.filter(slug=unique_slug).exists():
			postfix_size = len(str(num)) + 1
			unique_slug = '{}-{}'.format(
				slug[:(slug_max_size - postfix_size)], num
			)
			num += 1

		return unique_slug

	def save(self, *args, **kwargs):

		if not self.slug:
			self.slug = self._get_unique_slug()

		super().save(*args, **kwargs)


class Article(models.Model):
	title = models.CharField(
		'Заголовок', max_length=255, unique=True, null=False
	)
	slug = models.SlugField(unique=True, null=False, blank=True)
	body = models.TextField('Текст', null=False)
	preview = models.TextField('Превью', null=False)
	created_at = models.DateTimeField('Создана', blank=True)
	pub_date = models.DateTimeField('Дата публикации', blank=True)
	tags = models.ManyToManyField(Tag, verbose_name='Теги')

	def __str__(self):
		return self.title

	def _get_unique_slug(self):
		slug_max_size = 50
		slug = slugify(self.title)[:slug_max_size]
		unique_slug = slug
		num = 1

		while Article.objects.filter(slug=unique_slug).exists():
			postfix_size = len(str(num)) + 1
			unique_slug = '{}-{}'.format(
				slug[:(slug_max_size - postfix_size)], num
			)
			num += 1

		return unique_slug

	def was_published_recently(self):
		now = timezone.now()
		# noinspection PyTypeChecker
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Опубликовано недавно?'

	class Meta:
		verbose_name = "Пост"
		verbose_name_plural = "Посты"

	def save(self, *args, **kwargs):

		if not self.slug:
			self.slug = self._get_unique_slug()

		if self.pk is None:
			if self.created_at is None:
				self.created_at = timezone.now()

			if self.pub_date is None:
				self.pub_date = timezone.now()

		super().save(*args, **kwargs)


class Comment(models.Model):
	body = models.TextField('Текст', null=False)
	nickname = models.CharField('Ник', null=False, max_length=255)
	datetime = models.DateTimeField('Дата', null=False, blank=True)
	article = models.ForeignKey(
		'Article', on_delete=models.CASCADE, null=False
	)

	def save(self, *args, **kwargs):

		if self.pk is None:
			if self.datetime is None:
				self.datetime = timezone.now()

		super().save(*args, **kwargs)

	class Meta:
		verbose_name = "Комментарий"
		verbose_name_plural = "Комментарии"
