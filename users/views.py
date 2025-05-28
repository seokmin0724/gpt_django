from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import SignUpForm

def login_view(request):
    if request.method == "POST": #요청받은 메소드가 포스트일때
        username = request.POST.get("username") # post 요청해서  유저이름을 가져옴
        password = request.POST.get("password")# post 요청해서 비밀번호를 가져옴
        user = authenticate(request, username=username, password=password) #사용자 인증
        if user : # 사용자가 인증 되어있는지 확인
            auth_login(request, user) # 로그인 처리
            return redirect("index")  # 로그인 성공 후 이동할 페이지
    else: # 그렇지 않으면
            return render(request, "login.html", {"error": "Invalid credentials"}) # 로그인 실패 시, 에러 메시지를 전달하며 login.html 페이지 렌더링
    return render(request, "login.html") # login.html 페이지 렌더링

def logout_view(request):
    auth_logout(request)    #사용자 로그아웃 (세션종료)
    return redirect("login")  # 로그아웃 후 이동할 페이지

def signup_view(request):
    if request.method == "POST": #요청받은 메소드가 포스트일때
        form = SignUpForm(request.POST)  # POST 요청에서 전달받은 데이터를 이용해 회원가입 폼 생성
        if form.is_valid(): #폼 유효성 검사
            user = form.save()# 유효하면 사용자 정보 저장
            auth_login(request, user)# 저장 후 로그인 처리
            return redirect("login")  # 회원가입 후 이동할 페이지
    else: #그렇지 않으면
        form = SignUpForm()# 빈 회원가입 폼 생성
    return render(request, "signup.html", {"form": form})# signup.html 페이지에 폼 전달하여 렌더링
