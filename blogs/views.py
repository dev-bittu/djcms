from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import F
from .models import Blog, Comment, Reply, Bookmark

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
    def get(self, request):
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.GET.get("id")))
        return redirect("blogs:blog", slug=blog.slug)

    def post(self, request):
        if request.user.is_anonymous:
            messages.warning(request, "Need to login first")
            return redirect("index")
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        comment = request.POST.get("comment")
        if not comment:
            messages.warning(request, "Comment required")
            redirect("blogs:blog", slug=blog.slug)
        c = Comment(
            comment = comment,
            creator = request.user,
            blog = blog
        )
        c.save()
        messages.success(request, "Comment created")
        return redirect("blogs:blog", slug=blog.slug)

class CreateReply(View):
    def get(self, request):
        comment = get_object_or_404(Comment.objects.filter(is_active=True, id=request.GET.get("id")))
        return redirect("blogs:blog", slug=comment.blog.slug)

    def post(self, request):
        if request.user.is_anonymous:
            messages.warning(request, "You are not aithenticated")
            return redirect("index")
        comment = get_object_or_404(Comment.objects.filter(is_active=True, id=request.POST.get("id")))
        reply = request.POST.get("reply")
        if not reply:
            messages.warning(request, "Reply required")
            return redirect("blogs:blog", slug=comment.blog.slug)

        r = Reply(
            reply = request.POST.get("reply", ""),
            comment = comment,
            creator = request.user
        )
        r.save()

        messages.success(request, "Reply created")
        return redirect("blogs:blog", slug=comment.blog.slug)

class CreateBookmark(View):
    def post(self, request):
        if request.user.is_anonymous:
            messages.warning(request, "login required")
            return redirect("accounts:login")
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        b = Bookmark.objects.filter(creator=request.user, blog=blog).first()
        if b:
            messages.info(request, "Already bookmarked this blog")
        else:
            b = Bookmark(
                blog = blog,
                creator = request.user
            )
            b.save()
            messages.success(request, "Bookmark created")
        return redirect("blogs:blog", slug=blog.slug)
