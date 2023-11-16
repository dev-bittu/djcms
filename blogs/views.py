from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.db.models import F
from django.urls import reverse
from .models import *

# Create your views here.
def get_blog_url(slug):
    return reverse("blogs:blog", args=[slug])

class BlogView(View):
    def get(self, request, slug):
        queryset = Blog.objects.filter(is_active=True, slug=slug)
        blog = get_object_or_404(queryset)
        blog.views = F("views") + 1
        blog.save()
        blog.refresh_from_db()

        context = {
            "blog": blog,
            "comments": blog.comments.filter(is_active=True)
        }
        if request.user.is_authenticated:
            context["bookmarked"] = Bookmark.objects.filter(creator=request.user, blog=blog).first()
            context["liked"] = BlogLike.objects.filter(blog=blog, creator=request.user).first()

        return render(request, "blogs/blog.html", context)

class CreateComment(View):
    def post(self, request):
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        comment = request.POST.get("comment")
        if not comment:
            messages.warning(request, "Comment required")
            return redirect("blogs:blog", slug=blog.slug)
        c = Comment(
            comment = comment,
            creator = request.user,
            blog = blog
        )
        c.save()
        messages.success(request, "Comment created")
        return redirect(get_blog_url(blog.slug)+"#comments")

class CreateReply(View):
    def post(self, request):
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
        return redirect(get_blog_url(comment.blog.slug)+"#comments")

class CreateBookmark(View):
    def post(self, request):
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        bookmarked = Bookmark.objects.filter(creator=request.user, blog=blog).first()
        if bookmarked:
            messages.info(request, "Already bookmarked this blog")
        else:
            b = Bookmark(
                blog = blog,
                creator = request.user
            )
            b.save()
            messages.success(request, "Bookmark created")
        return redirect("blogs:blog", slug=blog.slug)

class CreateLike(View):
    def post(self, request):
        blog = get_object_or_404(Blog.objects.filter(is_active=True, id=request.POST.get("id")))
        liked = BlogLike.objects.filter(blog=blog, creator=request.user).first()
        if liked:
            messages.info(request, "You are already liked this post")
        else:
            l = BlogLike(creator=request.user, blog=blog)
            l.save()
            messages.success(request, "Liked this blog")
        return redirect(get_blog_url(blog.slug)+"#features")
