from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import F
from .models import Blog, Comment

# Create your views here.
class BlogView(View):
    def get(self, request, slug):
        queryset = Blog.objects.filter(is_active=True, slug=slug)
        blog = get_object_or_404(queryset)
        blog.views = F("views") + 1
        blog.save()
        blog.refresh_from_db()
        comments = blog.comments.filter(is_active=True)
        return render(request, "blogs/blog.html", {"blog": blog, "comments": comments})

class CreateComment(View):
    def post(self, request):
        if request.user.is_anonymous:
            messages.warning(request, "Need to login first")
            return redirect("index")
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        c = Comment(
            comment = request.POST.get("comment", ""),
            creator = request.user,
            blog = blog
        )
        c.save()
        messages.success(request, "Comment created")
        return redirect("blogs:blog", slug=blog.slug)

