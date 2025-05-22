from django.views.generic import DetailView, TemplateView
from django.shortcuts import get_object_or_404
from restaurans.models import Restaurans
from menu.models import Dish, Categories, LabelPreference


class MenuView(TemplateView):
    template_name = 'menu/restaurant_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_slug = self.kwargs.get('restaurant_slug')

        # Получаем ресторан
        restaurant = get_object_or_404(Restaurans, slug=restaurant_slug)
        context['restaurant'] = restaurant
        context['title'] = restaurant.name

        # Получаем блюда и категории
        dishes = Dish.objects.filter(restaurant=restaurant).prefetch_related('labels')
        categories = Categories.objects.filter(dish__in=dishes).distinct()

        # Сортируем блюда по категориям
        dishes_by_category = {
            category: dishes.filter(category=category) for category in categories
        }

        context['categories'] = categories
        context['dishes_by_category'] = dishes_by_category

        # Если пользователь авторизован — добавим его предпочтения
        user = self.request.user
        if user.is_authenticated:
            context['liked_ingredients'] = set(map(str.strip, (user.liked_ingredients or '').lower().split(',')))
            context['disliked_ingredients'] = set(map(str.strip, (user.disliked_ingredients or '').lower().split(',')))

            preferences = LabelPreference.objects.filter(user=user).select_related('label')
            context['liked_labels'] = set(p.label for p in preferences if p.preference_type == 'like')
            context['disliked_labels'] = set(p.label for p in preferences if p.preference_type == 'dislike')
        else:
            context['liked_ingredients'] = set()
            context['disliked_ingredients'] = set()
            context['liked_labels'] = set()
            context['disliked_labels'] = set()

        return context


class DishDetailView(DetailView):
    model = Dish
    template_name = 'includes/modal_dish.html'
    context_object_name = 'dish'

    def get_object(self):
        dish_id = self.kwargs.get('dish_id')
        return get_object_or_404(Dish, id=dish_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_type'] = 'dish'
        return context
