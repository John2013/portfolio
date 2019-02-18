from django.db import models
from django.utils.text import slugify

from blog.models import Tag


class Work(models.Model):
	name = models.CharField(
		'Название', max_length=255, null=False, default='', unique=True
	)
	url = models.URLField()
	url_source = models.URLField('URL исходников', null=True)
	short_description = models.TextField('Краткое описание', max_length=63)
	description = models.TextField('Описание')
	image = models.ImageField('Изображение')
	slug = models.SlugField(null=False, default='', unique=True, blank=True)

	tags = models.ManyToManyField(Tag, verbose_name='Теги')

	created_at = models.DateTimeField('Создано', auto_now_add=True)
	updated_at = models.DateTimeField('Изменено', auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Работа"
		verbose_name_plural = "Работы"

	def _get_unique_slug(self, slug_max_length=50):
		slug_max_size = slug_max_length
		slug = slugify(self.name, allow_unicode=True)[:slug_max_size]
		unique_slug = slug
		num = 1

		while Work.objects.filter(slug=unique_slug).exists():
			# обрезаем размер слага, чтобы он влез в поле
			postfix_size = len(str(num)) + 1
			unique_slug = '{}-{}'.format(
				slug[:(slug_max_size - postfix_size)], num
			)
			num += 1

		return unique_slug

	def save(self, *args, **kwargs):
		self.slug = self._get_unique_slug()

		super().save(*args, **kwargs)

