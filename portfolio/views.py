from django.shortcuts import render


def index(request):
	return render(request, 'portfolio/work_index.html')
