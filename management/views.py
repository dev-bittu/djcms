from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from blogs.models import Category, Blog
from django.utils import timezone
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
        status = data.get("status")

        if not (title and desc and content and thumbnail and categories and status):
            messages.info(request, "title, desc, content, thumbnail, categories, or status can't be empty")
            return redirect("manage:add_blog")

        try:
            status = bool(int(status))
        except:
            messages.info(request, "Something wrong with status")
            return redirect("manage:add_blog")

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

        return redirect("manage:add_blog")


class AddCategory(View):
    def get(self, request):
        return render(request, "management/add_category.html")

    def post(self, request):
        data = request.POST
        category = data.get("category")
        desc = data.get("desc")

        c = Category.objects.filter(category=category).first()
        if c is not None:
            messages.warn(request, "Category already exists")
        else:
            c = Category(
                category=category,
                desc=desc
            )
            c.save()
            messages.success(request, "Category created")
        return redirect("manage:add_category")
        

@method_decorator(login_required, name="dispatch")
class DraftBlogs(View):
    def get(self, request):
        if not request.user.is_author:
            messages.info(request, "You are not an author")
            return redirect("index")
        draft = Blog.objects.filter(is_active=True, is_published=False, creator=request.user)
        return render(request, "management/draft_blogs.html", {"draft": draft})

@method_decorator(login_required, name="dispatch")
class UpdateBlog(View):
    def get(self, request):
        if not request.user.is_author:
            messages.info(request, "You are not an author")
            return redirect("index")
        blogs = Blog.objects.filter(is_active=True)
        return render(request, "management/update.html", {"blogs": blogs})

@method_decorator(login_required, name="dispatch")
class EditBlog(View):
    def get(self, request, id):
        if not request.user.is_author:
            messages.info(request, "You are not an author")
            return redirect("index")
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.info(request, "Blog not exists")
            return redirect("manage:update_blog")
        categories = Category.objects.all()
        form = CKEditorForm({"content": blog.content})
        return render(request, "management/edit.html", {"blog": blog, "categories": categories, "form": form})
    
    def post(self, request, id = None):
        data = request.POST
        id = data.get("id")
        blog = Blog.objects.filter(is_active=True, creator=request.user, id=id).first()
        if blog is None:
            messages.info(request, "Blog doesn't exists")
            return redirect("manage:update_blog")

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
        
        for id in categories:
            try:
                c = Category.objects.get(id=int(id))
                blog.categories.add(c)
            except Exception as e:
                pass

        blog.save()
        messages.success(request, "Changes saved")

        return redirect("manage:update_blog")

class DeleteBlogs(View):
    def get(self, request):
        return render(request, "management/delete_blogs.html", {"blogs": Blog.objects.filter(is_active=True)})

class DeleteBlog(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.warn(request, "Blog doesn't exists")
        else:
            blog.is_active = False
            blog.save()
            messages.info(request, "Blog deleted")

        return redirect("manage:delete_blog")
