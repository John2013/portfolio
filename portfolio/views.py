from django.shortcuts import render
from django.views.generic import ListView

from portfolio.models import Work


def index(request):
	return render(request, 'portfolio/work_list.html')


class WorksList(ListView):
	model = Work
