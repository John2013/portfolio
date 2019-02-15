from django.contrib import admin

from .models import Article, Tag, Comment


class ArticleAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['title', 'preview', 'body', 'slug']}),
		(
			'Теги',
			{'fields': ['tags']}
		),
		(
			'Даты',
			{'fields': ['created_at', 'pub_date'], 'classes': ['collapse']}
		),
	]
	filter_horizontal = ('tags', )
	list_display = ('title', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['title', 'preview', 'body']


class TagsAdmin(admin.ModelAdmin):
	search_fields = ['name']
	list_display = ('name', 'slug')
	fields = ('name', 'slug')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Comment)
