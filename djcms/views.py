from django.shortcuts import render
from django.views import View
from blogs.models import Blog

class Index(View):
    def get(self, request):
        latest_blogs = Blog.objects.all()[:6]
        return render(request, "index.html", {"latest": latest_blogs})

class Trendings(View):
    def get(self, request):
        trendings = Blog.objects.order_by("-views")[:10]
        return render(request, "trendings.html", {"trendings": trendings})

class Latest(View):
    def get(self, request):
        latest = Blog.objects.order_by("-published_on")[:10]
        return render(request, "latest.html", {"latest": latest})
