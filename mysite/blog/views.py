from django.views import generic
from .models import Article


class IndexView(generic.ListView):
	model = Article
	paginate_by = 10
	ordering = ['-pk']


class TagView(IndexView):
	def get_queryset(self):
		return Article.objects.filter(tags__slug__contains=self.kwargs['tag'])


class DetailView(generic.DetailView):
	model = Article

	def get_queryset(self):
		return Article.objects.filter(slug=self.kwargs['slug'])
