from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import SignUpForm

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user :
            auth_login(request, user)
            return redirect("index")  # 로그인 성공 후 이동할 페이지
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("login")  # 로그아웃 후 이동할 페이지

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("login")  # 회원가입 후 이동할 페이지
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})
