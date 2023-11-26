from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from blogs.models import Category, Blog, Comment
from django.utils import timezone
from .forms import CKEditorForm

# Create your views here.
class ManageBlog(View):
    def get(self, request):
        blogs = Blog.objects.filter(is_active=True, creator=request.user)
        return render(request, "management/blog.html", {"blogs": blogs})

class ManageCategory(View):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        return render(request, "management/category.html", {"categories": categories})


class CreateBlog(View):
    def get(self, request):
        form = CKEditorForm()
        categories = Category.objects.filter(is_active=True)
        return render(request, "management/create_blog.html", {"form": form, "categories": categories})

    def post(self, request):
        data = request.POST
        title = data.get("title")
        desc = data.get("desc")
        content = data.get("content")
        thumbnail = request.FILES.get("thumbnail")
        categories = data.getlist("categories") 
        status = data.get("status")

        if not (title and desc and content and thumbnail and categories and status):
            messages.info(request, "title, desc, content, thumbnail, categories, or status can't be empty")
            return redirect("manage:create_blog")

        try:
            status = bool(int(status))
        except:
            messages.info(request, "Something wrong with status")
            return redirect("manage:create_blog")

        blog = Blog(
            title = title,
            desc = desc,
            content = content,
            creator = request.user,
            thumbnail = thumbnail,
            is_published = status
        )
        blog.save()
        for id in categories:
            try:
                c = Category.objects.get(id=int(id))
                blog.categories.add(c)
            except Exception as e:
                pass

        blog.save()
        messages.success(request, "Blog created")

        return redirect("manage:create_blog")


class CreateCategory(View):
    def get(self, request):
        return render(request, "management/create_category.html")

    def post(self, request):
        data = request.POST
        category = data.get("category")
        desc = data.get("desc")

        c = Category.objects.filter(category=category).first()
        if c is not None:
            messages.warning(request, "Category already exists")
        else:
            c = Category(
                category=category,
                desc=desc
            )
            c.save()
            messages.success(request, "Category created")
        return redirect("manage:create_category")
        
class EditBlog(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.info(request, "Blog not exists")
            return redirect("manage:blog")
        categories = Category.objects.all()
        form = CKEditorForm({"content": blog.content})
        return render(request, "management/edit_blog.html", {"blog": blog, "categories": categories, "form": form})
    
    def post(self, request, id = None):
        data = request.POST
        id = data.get("id")
        blog = Blog.objects.filter(is_active=True, creator=request.user, id=id).first()
        if blog is None:
            messages.info(request, "Blog doesn't exists")
            return redirect("manage:blog")

        title = data.get("title")
        desc = data.get("desc")
        content = data.get("content")
        status = data.get("status")
        thumbnail = request.FILES.get("thumbnail")
        categories = data.getlist("categories")

        blog.title = title
        blog.desc = desc
        blog.content = content
        if thumbnail:
            blog.thumbnail = thumbnail

        try:
            status = int(status)
            if not blog.is_published and status:
                blog.published_on = timezone.now()
            blog.is_published = bool(status)
        except:
            messages.info(request, "Error while updating status")
        
        blog.categories.set([])
        for id in categories:
            try:
                c = Category.objects.get(id=int(id))
                blog.categories.add(c)
            except Exception as e:
                pass

        blog.save()
        messages.success(request, "Changes saved")

        return redirect("manage:blog")

class DeleteBlog(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.warning(request, "Blog doesn't exists")
        else:
            blog.is_active = False
            blog.save()
            messages.info(request, "Blog deleted")

        return redirect("manage:blog")

class EditCategory(View):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id, is_active=True)
        return render(request, "management/edit_category.html", {"category": category})

    def post(self, request, id):
        c = Category.objects.filter(id=id, is_active=True).first()
        data = request.POST
        category, desc = data.get("category"), data.get("desc")
        if not ((category and desc) or c):
            messages.warning(request, "Category or Desc can't be empty. OR Category doesn't exists")
            return redirect("manage:category")
        c.category = category
        c.desc = desc
        c.save()
        messages.success(request, "Changes saved")
        return redirect("manage:category")
        

class DeleteCategory(View):
    def get(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.is_active = False
        category.save()
        messages.info(request, "Category removed")
        return redirect("manage:category")

class ManageComment(View):
    def get(self, request):
        comments = Comment.objects.filter(is_active=True, blog__in=Blog.objects.filter(creator=request.user))
        return render(request, "management/comment.html", {"comments": comments})

class DeleteComment(View):
    def get(self, request, id):
        comment = get_object_or_404(Comment.objects.filter(id=id, is_active=True))
        if comment.blog.creator.username != request.user.username:
            messages.warning(request, "You are not author of that blog")
            return redirect("manage:comment")
        comment.is_active = False
        comment.save()
        messages.success(request, "Comment deleted")
        return redirect("manage:comment")
