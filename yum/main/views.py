from django.shortcuts import render

from restaurans.models import Restaurans


# Create your views here.
def index(request):
	restaurans = Restaurans.objects.all()

	context = {
		'title' : "Главная страница | YUM",
		'restaurans' : restaurans,
	}
	return render(request, 'main/index.html', context)

def about(request):
	context = {
		'title' : "О нас | YUM"
	}
	return render(request, 'main/about.html', context)

