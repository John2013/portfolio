from django import template
from django.urls import reverse, resolve

register = template.Library()


@register.inclusion_tag('main_menu.html')
def main_menu(request):
	current_url = resolve(request.path_info).url_name
	items = [
		('Блог', reverse('blog:index')),
		('Портфолио', reverse('portfolio:index'))
	]

	def menu_item_append_active(item):
		title, url = item
		return title, url, resolve(url) == current_url

	items = map(
		menu_item_append_active,
		items
	)
	return {'items': items}
