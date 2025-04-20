from django.contrib import admin

from promotions.models import Promotion, PromotionRequest


# Register your models here.

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'start_time', 'end_time')

@admin.register(PromotionRequest)
class PromotionRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'is_paid', 'is_approved', 'created_at')
    list_filter = ('is_paid', 'is_approved')
    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        for req in queryset.filter(is_paid=True, is_approved=False):
            Promotion.objects.create(
                restaurant=req.restaurant,
                name=req.name,
                description=req.description,
                start_time=req.start_time,
                end_time=req.end_time,
                image=req.image
            )
            req.is_approved = True
            req.save()
        self.message_user(request, "Выбранные заявки одобрены и опубликованы.")
