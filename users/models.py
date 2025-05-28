from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 사용자 모델을 정의하는 파일입니다.
# 사용자 모델을 정의하기 위해 Django의 AbstractBaseUser와 PermissionsMixin을 상속받습니다.
# AbstractBaseUser는 기본적인 사용자 모델을 제공하고, PermissionsMixin은 권한 관련 기능을 추가합니다.
class UserManager(BaseUserManager):
    def create_user(self, username, email=None ,password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(username=username)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(username, password, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)  # 관리자인지 여부
    is_active = models.BooleanField(default=True)

    objects = UserManager()  # 사용자 매니저 설정

    USERNAME_FIELD = 'username'  # 사용자 이름 필드
    REQUIRED_FIELDS = []  # createsuperuser 시 요구할 필드
    def __str__(self):
        return self.username