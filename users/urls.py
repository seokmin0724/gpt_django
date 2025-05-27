from django.shortcuts import render, redirect
from django.urls import path
from users.models import User
from django.contrib.auth import login as auth_login
from django.urls import path
from django.contrib.auth import login as auth_login, logout as auth_logout  # 추가

from users.views import logout


def index(request):
    if request.user.is_authenticated:
        # 사용자가 로그인한 경우
        return render(request, "index.html", {"username": request.user.username})
    else:
        # 사용자가 로그인하지 않은 경우
        return redirect("login")

def login(request):
    # 사용자가 로그인 정보를 입력하여 전송했을 때 (POST 요청)
    if request.method == "POST": #메소드가 포스트면 조건문 실행
        username = request.POST.get("username")  # 폼에서 입력한 사용자명
        password = request.POST.get("password")  # 폼에서 입력한 비밀번호

        try:
            user = User.objects.get(username=username)  # 사용자 검색
            if user.check_password(password):  # 비밀번호 확인
                auth_login(request, user)  # 로그인 처리
                # 로그인 성공 -> index.html 렌더링
                return redirect("index") # 반환한다...
            else:
                # 비밀번호가 틀린 경우 -> 에러 메시지 포함하여 로그인 폼 다시 표시
                return render(request, "login.html", {"error": "비밀번호 틀렸습니다."})
        except User.DoesNotExist:   #시도했을 때 예외적으로 없으면 에러를 반환하는 ...
            # 사용자가 존재하지 않는 경우 -> 에러 메시지 포함하여 로그인 폼 다시 표시
            return render(request, "login.html", {"error": "User does not exist"})

    # 이 부분이 없어서 오류가 발생했던 것! => GET 요청 처리
    # 사용자가 로그인 페이지에 접근했을 때 (예: 링크 클릭 등)
    return render(request, "login.html")



urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),  # 로그아웃 URL 추가
]