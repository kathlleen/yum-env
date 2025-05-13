from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from restaurans.models import Restaurans
from menu.models import Categories
from promotions.models import Promotion
from main.utils import q_search

from django.views.generic import TemplateView
from restaurans.models import Cuisine
from promotions.models import PromotionRequest
from rest_collections.models import Selection


# Create your views here.
class IndexView(TemplateView):
	template_name = 'main/index.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category_slug = self.kwargs.get('category_slug', 'all')
		query = self.request.GET.get('q', None)

		# Получение категорий
		categories = Categories.objects.all()
		context['categories'] = categories
		context['sliced_categories'] = categories[:10]

		# Логика выбора ресторанов
		if query:
			restaurans = q_search(query)
		elif category_slug == 'all':
			restaurans = Restaurans.objects.all()
		else:
			restaurans = Restaurans.objects.filter(restaurant__category__slug=category_slug).distinct()

		# После получения queryset
		restaurans = list(restaurans)

		# Сортировка: сначала открытые, потом закрытые

		# !!! Добавить кэширование с обновлением раз в пол часа !!!
		restaurans.sort(key=lambda r: (not r.is_open(), r.name))
		context['restaurans'] = restaurans

		# Получение акций
		# !!! Добавить кэширование с обновлением раз в день !!!
		promotions = PromotionRequest.objects.filter(is_approved=True).filter(is_active=True)
		context['promotions'] = promotions

		# Заголовок страницы
		context['title'] = "Главная страница | YUM"
		context['cuisines'] = Cuisine.objects.all()

		# !!! Добавить кэширование запроса с обновлением раз в день !!!
		context['best_rest'] = Restaurans.objects.order_by("-rating")[:20]
		context['selections'] = Selection.objects.all()
		return context

def filter_restaurants(request, category_slug):
	if category_slug == 'all':
		restaurans = Restaurans.objects.all()
	else:
		restaurans = Restaurans.objects.filter(restaurant__category__slug=category_slug).distinct()

	# Рендерим только частичку HTML с ресторанами
	html = render(request, 'includes/restaurants_list.html', {'restaurans': restaurans}).content.decode('utf-8')
	return JsonResponse({'html': html})

def filter_by_cuisine(request, cuisine_slug):
	restaurans = Restaurans.objects.filter(cuisine__slug=cuisine_slug).distinct()

	html = render(request, 'includes/restaurants_list.html', {'restaurans': restaurans}).content.decode('utf-8')
	return JsonResponse({'html': html})

def about(request):
	context = {
		'title' : "О нас | YUM"
	}
	return render(request, 'main/about.html', context)

def promotion_detail(request, promo_id):
	promotion = get_object_or_404(PromotionRequest, id=promo_id)
	print(f"Promotion ID: {promotion.id}, Name: {promotion.name}")  # Отладочная информация
	return render(request, 'includes/modal_promotion.html', {'promotion': promotion, 'content_type': 'promotion'})

def cart_detail(request):
	return render(request, 'includes/all_carts.html', {'content_type': 'cart'})