from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import F
from .models import Blog

# Create your views here.
class BlogView(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        blog.views = F("views") + 1
        blog.save()
        return render(request, "blogs/blog.html", {"blog": blog})
