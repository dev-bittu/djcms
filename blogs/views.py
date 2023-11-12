from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.db.models import F
from .models import Blog

# Create your views here.
class BlogView(View):
    def get(self, request, slug):
        blog = Blog.objects.filter(slug=slug, is_active=True).first()
        if blog is None:
            messages.info(request, "Blog doesnt exists")
            return redirect("index")
        blog.views = F("views") + 1
        blog.save()
        blog.refresh_from_db()
        return render(request, "blogs/blog.html", {"blog": blog})
