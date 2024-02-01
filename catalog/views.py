from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Blog, Version, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache import cache

from django.contrib.auth.models import Permission

from catalog.services import get_cached_categories
from users.models import User


@login_required
@cache_page(60)
def index(request):
    return render(request, 'catalog/index.html')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/catalog_of_products.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # active_versions = Version.objects.filter(is_active=True)
        # context['active_versions'] = active_versions
        context['category'] = get_cached_categories()  # используем сервисную функцию
        return context


class CategoriesListView(ListView):
    model = Category


def categories(request):
    context = {
        'object_list': get_cached_categories(),
        'title': 'Все категории'
    }
    return render(request, 'catalog/categories.html', context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog_of_products')

    def form_valid(self, form):
        self.object = form.save()
        self.object.proprietor = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog_of_products')

    def form_valid(self, form):
        self.object = form.save()
        if self.request.user != self.object.proprietor:
            reverse_lazy('catalog:catalog_of_products')
            print('это не твой продукт брысь')
            form.add_error(None, 'это не твой продукт брысь')
            return super().form_invalid(form)
        self.object.proprietor = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_details', args=[self.kwargs.get('pk')])


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_details.html'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:catalog_of_products')


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('header', 'text', 'preview',)
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.header)
            new_post.save()
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'catalog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('header', 'slug', 'text', 'preview')

    def get_success_url(self):
        return reverse_lazy('catalog:blog_details', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.header)
            new_post.save()
        return super().form_valid(form)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = 'catalog/blog_details.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        print(self.object.views_count)
        self.object.views_count = int(self.object.views_count) + 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:version_list')


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    template_name = 'catalog/version_list.html'


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')


class VersionDeleteView(DeleteView):
    model = Version
    success_url = reverse_lazy('catalog:index')
