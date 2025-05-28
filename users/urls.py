from django.shortcuts import render, redirect
from django.urls import path
from users.views import login_view, logout_view, signup_view  # 올바르게 임포트

def index(request):
    if request.user.is_authenticated: #사용자 있을 경우에 로그인..
        # 사용자가 로그인한 경우
        return render(request, "index.html", {"username": request.user.username})
    else:
        # 사용자가 로그인하지 않은 경우
        return redirect("login")






urlpatterns = [

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # 로그아웃 URL 추가
    path('signup/', signup_view, name='signup'),
    path('', index, name='index'),
]