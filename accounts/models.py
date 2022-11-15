from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create account Manager.
class MyAccountManager(BaseUserManager):
    # Create user.
    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not email:
            raise ValueError('User must have email address')
        if not user_name:
            raise ValueError('Please enter your name')
        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create Super user.
    def create_superuser(self, first_name, last_name, user_name, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create user Model
class Account(AbstractBaseUser):
    # Create user Field

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50, unique=True)

    # Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Make the Email user name to login
    USERNAME_FIELD = 'email'

    # the required fields
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # defining some mandatory methods that configure the user if it is an admin or not

    def has_perm(self, prem, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
