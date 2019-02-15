from django import template

register = template.Library()


@register.inclusion_tag('main_menu.html')
def main_menu():
	items = []
	return {'items': items}
