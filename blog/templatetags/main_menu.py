from django import template
from django.urls import reverse, resolve

register = template.Library()


@register.inclusion_tag('main_menu.html')
def main_menu(request):
	current_view_name = resolve(request.path_info).view_name
	items = [
		('Блог', 'blog:index'),
		('Портфолио', 'portfolio:index')
	]

	def menu_item_append_active(item):
		title, view_name = item
		return title, view_name, view_name == current_view_name

	def menu_item_reverse_url(item):
		title, view_name = item
		return title, reverse(view_name)

	def process_menu_item(item):
		item = tuple(menu_item_append_active(item))
		item = tuple(menu_item_reverse_url(item))
		return item

	items = map(
		process_menu_item,
		items
	)
	return {'items': items}
