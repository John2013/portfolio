from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('main_menu.html')
def main_menu():
	items = [
		('Блог', reverse('blog:index'), True),
		('Портфолио', reverse('portfolio:index'), False)
	]
	return {'items': items}
