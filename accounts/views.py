from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in, Logout first")
            return redirect("index")
        return render(request, "accounts/login.html")

    def post(self, request):
        uname = request.POST.get("username", "")
        passwd = request.POST.get("password", "")
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in")
            return redirect("index")
        else:
            messages.warning(request, "Username or password is incorrect")
        return render(request, "accounts/login.html")

@method_decorator(login_required, name="dispatch")
class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out")
        return redirect("accounts:login")

class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in")
            return redirect("index")
        return render(request, "accounts/register.html")
    
    def post(self, request):
        data = request.POST
        passwd1 = data.get("password1", "")
        passwd2 = data.get("password2","")
        if passwd1 and (passwd1 != passwd2):
            messages.warning(request, "Passwords do not match")
            return redirect("accounts:register")
        
        email, username, firstname = data.get("email"), data.get("username"), data.get("firstname")
        if not (email and username and firstname):
            messages.info(request, "Email, username, and first name required")
            return redirect("accounts:register")
        
        user = User.objects.filter(Q(email=email) | Q(username=username))
        if not user.exists():
            user = User(email=email, username=username, first_name=firstname)
            if lastname := data.get("lastname"):
                user.last_name = lastname
            user.set_password(passwd1)
            user.save()
            messages.success(request, "User created")
            login(request, user)
            messages.success(request, "Logged in")
            return redirect("index")

        messages.info(request, "User already exists")
        return redirect("accounts:register")
