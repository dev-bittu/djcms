from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import F
from .models import Blog

# Create your views here.
class BlogView(View):
    def get(self, request, slug):
        queryset = Blog.objects.filter(is_active=True, slug=slug)
        blog = get_object_or_404(queryset)
        blog.views = F("views") + 1
        blog.save()
        blog.refresh_from_db()
        return render(request, "blogs/blog.html", {"blog": blog})
