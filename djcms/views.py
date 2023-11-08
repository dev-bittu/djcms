from django.shortcuts import render
from django.views import View
from blogs.models import Blog

class Index(View):
    def get(self, request):
        return render(request, "index.html")

class Trendings(View):
    def get(self, request):
        trendings = Blog.objects.all()[:10]
        return render(request, "trendings.html", {"trendings": trendings})
