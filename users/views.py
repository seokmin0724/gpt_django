from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
def logout(request):
    auth_logout(request)  # 사용자 세션에서 로그인 정보 삭제
    return redirect("login")  # 로그아웃 후 로그인 페이지로 리다이렉트
