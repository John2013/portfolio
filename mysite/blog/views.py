from django.views import generic
from .models import Article


class IndexView(generic.ListView):
	model = Article
	paginate_by = 10
