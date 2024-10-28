from django.shortcuts import render

from restaurans.models import Restaurans

from menu.models import Categories

from promotions.models import Promotion


# Create your views here.
def index(request, category_slug='all'):
	categories = Categories.objects.all()
	sliced_categories = list(categories[:10])

	if category_slug == 'all':
		restaurans = Restaurans.objects.all()
	else:
		restaurans = Restaurans.objects.filter(restaurant__category__slug=category_slug).distinct()

	promotions = Promotion.objects.all()

	context = {
		'title' : "Главная страница | YUM",
		'restaurans' : restaurans,
		'categories' : categories,
		'sliced_categories': sliced_categories,
		'promotions' : promotions,
	}
	return render(request, 'main/index.html', context)

def about(request):
	context = {
		'title' : "О нас | YUM"
	}
	return render(request, 'main/about.html', context)

