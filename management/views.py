from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from blogs.models import Category, Blog
from .forms import CKEditorForm

# Create your views here.
@method_decorator(login_required, name="dispatch")
class AddBlog(View):
    def get(self, request):
        if request.user.is_author:
            form = CKEditorForm()
            categories = Category.objects.all()
            return render(request, "management/add_blog.html", {"form": form, "categories": categories})
        messages.info(request, "You are not an author")
        return redirect("index")

    def post(self, request):
        if not request.user.is_author:
            messages.info(request, "You are not an author")
            return redirect("index")
        data = request.POST
        title = data.get("title")
        desc = data.get("desc")
        content = data.get("content")
        thumbnail = request.FILES.get("thumbnail")
        categories = data.getlist("categories") 

        if not (title and desc and content and thumbnail and categories):
            messages.info(request, "title, desc, content, thumbnail, or categories can't be empty")
            return redirect("manage:add_blog")

        blog = Blog(
            title = title,
            desc = desc,
            content = content,
            creator = request.user,
            thumbnail = thumbnail
        )

        for id in categories:
            try:
                c = Category.objects.get(id=int(id))
                blog.categories.add(c)
            except:
                continue

        blog.save()
        messages.success(request, "Blog created")

        return redirect("manage:add_blog")
