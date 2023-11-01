from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Blog

# Create your views here.
class BlogView(View):
    def get(self, request, slug):
        blog = Blog.objects.filter(slug=slug).first()
        if blog is None:
            messages.info(request, "Blog doesn't exists")
            return redirect("index")
        return render(request, "blogs/blog.html", {"blog": blog})
