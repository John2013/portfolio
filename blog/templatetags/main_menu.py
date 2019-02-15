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
	items = map(
		lambda title, url: (title, url, resolve(url) == current_url),
		items
	)
	return {'items': items}
