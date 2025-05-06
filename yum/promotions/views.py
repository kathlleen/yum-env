from django.shortcuts import render

# Create your views here.
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromotionRequestForm
from restaurans.models import Restaurans
from django.contrib import messages

from .models import Promotion, PromotionRequest


def promotion_request_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurans, id=restaurant_id)
    active_promotions = PromotionRequest.objects.filter(restaurant=restaurant)

    if request.method == "POST":
        form = PromotionRequestForm(request.POST, request.FILES)
        if form.is_valid():
            promo_req = form.save(commit=False)
            promo_req.restaurant = restaurant
            promo_req.save()
            # messages.success(request, "Заявка отправлена. Мы свяжемся с вами после проверки.")
            return redirect('restaurans:restaurant-dashboard')

    else:
        form = PromotionRequestForm()

    return render(request, 'promotions/promotion_request_form.html', {
        'form': form,
        'restaurant': restaurant,
        'active_promotions':active_promotions
    })

def edit_promotion(request, pk):
    promotion = get_object_or_404(PromotionRequest, pk=pk)
    if request.method == 'POST':
        form = PromotionRequestForm(request.POST, request.FILES, instance=promotion)
        if form.is_valid():
            form.save()
            return redirect('promotion_request')  # подставьте нужное имя
    else:
        form = PromotionRequestForm(instance=promotion)
    return render(request, 'edit_promotion.html', {'form': form})
