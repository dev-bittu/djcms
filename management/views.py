from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
@method_decorator(login_required, name="dispatch")
class AddBlog(View):
    def get(self, request):
        if request.user.is_author:
            return render(request, "management/add_blog.html")
        messages.info(request, "You are not an author")
        return redirect("index")
