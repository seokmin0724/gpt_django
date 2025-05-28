from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 사용자 모델을 정의하는 파일입니다.
# 사용자 모델을 정의하기 위해 Django의 AbstractBaseUser와 PermissionsMixin을 상속받습니다.
# AbstractBaseUser는 기본적인 사용자 모델을 제공하고, PermissionsMixin은 권한 관련 기능을 추가합니다.
class UserManager(BaseUserManager):
    def create_user(self, username, email ,password=None):
        if not username:
            raise ValueError("Users must have a username") #user name이 없으면 예외 발생
        if not email:
            raise ValueError("Users must have an email address")# 이메일이 없으면 예외 발생
        user = self.model(username=username)# 사용자 모델 인스턴스 생성
        user.set_password(password)  # 비밀번호 해싱하여 저장
        user.save(using=self._db) # 데이터베이스에 사용자 저장
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, password, email) # 일반 사용자  생성
        user.is_staff = True # 권리자 권한 부여
        user.is_superuser = True # 슈퍼유저 권한 부여
        user.save(using=self._db)# 데이터베이스에 저장
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)# 사용자 이름 고유값
    password = models.CharField(max_length=128)# 해싱된 상태로 저장
    email = models.EmailField(max_length=150, unique=True)# 이메일, 고유값
    is_staff = models.BooleanField(default=False) # 관리자인지 여부 (관리자 권한 체크용)
    is_active = models.BooleanField(default=True)# 활성화 여부(계정 활성 상태)

    objects = UserManager()  # 사용자 매니저 설정

    USERNAME_FIELD = 'username'  # 로그인 시 사용할 필드 설정
    REQUIRED_FIELDS = []  # createsuperuser 명령어 실행시 필수 입력필드
    def __str__(self):
        return self.username # 객체 출력 시 username 반환