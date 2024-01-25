from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Blog, Version


def index(request):
    return render(request, 'catalog/index.html')


class CatalogListView(ListView):
    model = Product
    template_name = 'catalog/catalog_of_products.html'
    # template_name = 'catalog/catalog_test.html'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:catalog_of_products')

    def form_validate(self, form):
        response = super().form_valid(form)
        self.object.proprietor = self.request.user
        self.object.save()
        return response


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_details.html'


class BlogCreateView(CreateView):
    model = Blog
    fields = ('header', 'text', 'preview',)
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.header)
            new_post.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'catalog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogUpdateView(UpdateView):
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


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'catalog/blog_details.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        print(self.object.views_count)
        self.object.views_count = int(self.object.views_count) + 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:version_list')


class VersionListView(ListView):
    model = Version
    template_name = 'catalog/version_list.html'


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')


class VersionDeleteView(DeleteView):
    model = Version
    success_url = reverse_lazy('catalog:index')