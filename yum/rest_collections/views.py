from django.http import JsonResponse
from django.shortcuts import render

from restaurans.models import Restaurans


# Create your views here.
def selection_restaurants(request, selection_slug):
	restaurans = Restaurans.objects.filter(
		selectionrestaurant__selection__slug=selection_slug
	).distinct()

	# Рендерим только частичку HTML с ресторанами
	html = render(request, 'includes/restaurants_list.html', {'restaurans': restaurans}).content.decode('utf-8')
	return JsonResponse({'html': html})