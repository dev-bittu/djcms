from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from blogs.models import Blog

class Index(View):
    def get(self, request):
        latest_blogs = Blog.objects.filter(is_active=True, is_published=True)[:6]
        popular = Blog.objects.filter(is_active=True, is_published=True).order_by("-views")[:3]
        return render(request, "index.html", {"latest": latest_blogs, "popular": popular})

class Trendings(View):
    def get(self, request):
        trendings = Blog.objects.filter(is_active=True, is_published=True).order_by("-views")[:10]
        return render(request, "trendings.html", {"trendings": trendings})

class Popular(View):
    def get(self, request):
        popular = Blog.objects.filter(is_active=True, is_published=True).order_by("-views")[:10]
        return render(request, "popular.html", {"popular": popular})

class Latest(ListView):
    model = Blog
    template_name = 'latest.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-published_on")

class Search(ListView):
    model = Blog
    template_name = "search.html"
    context_object_name = "blogs"
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get("query")
        blogs = Blog.objects.filter(
            (Q(title__icontains=query) | Q(desc__icontains=query)), is_active=True
        ).order_by("-views")
        return blogs

class Category(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, "category.html", {"categories": categories})

class GetCategory(View):
    def get(self, request, cat):
        category = get_object_or_404(Category, title=cat)
        return render(request, "get_category.html", {"category": category})
