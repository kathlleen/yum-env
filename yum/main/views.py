from django.shortcuts import render

from restaurans.models import Restaurans

from menu.models import Categories


# Create your views here.
def index(request):
	restaurans = Restaurans.objects.all()
	categories = Categories.objects.all()
	sliced_categories = list(categories[:10])

	context = {
		'title' : "Главная страница | YUM",
		'restaurans' : restaurans,
		'categories' : categories,
		'sliced_categories': sliced_categories,
	}
	return render(request, 'main/index.html', context)

def about(request):
	context = {
		'title' : "О нас | YUM"
	}
	return render(request, 'main/about.html', context)

