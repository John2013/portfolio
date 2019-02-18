from django.contrib import admin

from portfolio.models import Work


class WorkAdmin(admin.ModelAdmin):
	fieldsets = [
		(
			None,
			{'fields': [
				'name',
				'image',
				'url',
				'url_source',
				'slug'
			]}
		),
		(
			'Описание',
			{
				'fields': ['short_description', 'description'],
				'classes': ['collapse']
			}
		),
		(
			'Теги',
			{'fields': ['tags']}
		),
	]
	filter_horizontal = ('tags',)
	list_display = ('name', 'created_at', 'updated_at')
	list_filter = ['tags', 'created_at', 'updated_at']
	search_fields = ['name', 'short_description', 'description']


admin.site.register(Work, WorkAdmin)
