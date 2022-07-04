from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

"""Create your models here."""


class CustomUserManager(BaseUserManager):
    """
    Assignee : 희석

    custom user model 사용 시 UserManager 클래스와
    create_user, create_superuser 함수가 정의되어 있어야 함
    """

    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """python manage.py createsuperuser 사용 시 해당 함수가 사용됨"""
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    password = models.CharField("비밀번호", max_length=128)
    name = models.CharField("이름", max_length=20)
    mobile = models.CharField("휴대폰 번호", max_length=20)

    """is_active가 False일 경우 계정이 비활성화됨"""
    is_active = models.BooleanField("활성화", default=True)

    """is_staff에서 해당 값 사용"""
    is_admin = models.BooleanField("관리자", default=False)

    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    """"
    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    """
    USERNAME_FIELD = "email"

    """user를 생성할 때 입력받을 필드 지정"""
    REQUIRED_FIELDS = []

    """custom user 생성 시 필요"""
    objects = CustomUserManager()

    def __str__(self):
        return f"email: {self.email} / name: {self.name}"

    def has_perm(self, perm, obj=None):
        """
        # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
        # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
        """
        return True

    def has_module_perms(self, app_label):
        """ "
        # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
        # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
        """
        return True

    @property
    def is_staff(self):
        """admin 권한 설정"""
        return self.is_admin
