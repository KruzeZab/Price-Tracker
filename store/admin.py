from django.contrib import admin

from store.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'product_price', 'target_price']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'user']
    list_per_page = 50


admin.site.register(Product, ProductAdmin)
