from django.contrib import admin

from catalog.models import Product, Category, Blog, Version

# admin.site.register(Product)
# admin.site.register(Category)
"""Для моделей категории и продукта настройте отображение в административной панели. 
Для категорий выведите id и наименование в список отображения, а для продуктов выведите в список id, название, цену и категорию.
При этом интерфейс вывода продуктов настройте так, чтобы можно было результат отображения фильтровать по категории,
 а также осуществлять поиск по названию и полю описания."""


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'proprietor', )
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'views_count')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'version_name', 'is_active_version')
