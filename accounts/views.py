from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User

# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already login. Logout first")
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
        passwd1 = request.POST.get("password1", "")
        passwd2 = request.POST.get("password2","")
        if passwd1 != passwd2:
            messages.info(request, "Passwords don't match")
            return redirect("accounts:register")

        if not User.password_is_valid(passwd1):
            messages.info(request, "Password is not valid. It's length should be greater than 6")
            return redirect("accounts:register")
        
        uname = request.POST.get("username", "")
        email = request.POST.get("email", "")
        if not (uname or email):
            messages.warning(request, "Username or email can't be empty")
        if not User.email_is_valid(email):
            messages.warning(request, "Email is not valid")
            return redirect("accounts:register")
        
        user = User.objects.filter(Q(username=uname) | Q(email=email))
        if not user.exists():
            user = User(username=uname)
            user.set_password(passwd1)
            user.save()
            messages.success(request, "User created")
            login(request, user)
            messages.success(request, "Logged in")
            return redirect("index")

        messages.info("User already exists")
        return redirect("accounts:register")
