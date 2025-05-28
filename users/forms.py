from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ User를 get_user_model()로 가져옴

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 이메일 필드 추가, 필수 입력값으로 설정

    class Meta:
        model = User  # 폼과 연결된 사용자 모델 지정
        fields = ['username', 'email', 'password1', 'password2']  # 폼에서 사용할 필드 목록