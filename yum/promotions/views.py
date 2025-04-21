from django.shortcuts import render

# Create your views here.
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PromotionRequestForm
from restaurans.models import Restaurans
from django.contrib import messages

def promotion_request_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurans, id=restaurant_id)

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
    })
