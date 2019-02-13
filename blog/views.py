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
	article = None

	def get_queryset(self):
		self.article = Article.objects.filter(slug=self.kwargs['slug'])
		return self.article

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = self.article.get().comment_set.order_by(
			'datetime'
		).desc().all()
		return context
