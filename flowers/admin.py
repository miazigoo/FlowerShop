from django.contrib import admin
from django.http import HttpResponseRedirect

from flowers.models import Product, Order, ProductCategory, PriceCategory


@admin.register(ProductCategory)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(PriceCategory)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'from_price',
        'up_to_price',
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'firstname',
        'phone_number',
    ]
    list_display = [
        'firstname',
        'phone_number',
    ]
    readonly_fields = ['registration_date']

    def response_change(self, request, obj):
        res = super(OrderAdmin, self).response_post_save_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res


@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
    ]