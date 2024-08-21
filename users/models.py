from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class AccountManager(BaseUserManager):
    # needs to be named create_user
    def create_user(self, email, first_name, last_name, department, password=None, **other_fields):
        if not email:
            raise ValueError("Must have a valid email")
        
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            department=department,
            **other_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff(self, email, first_name, last_name, department, password=None, **other_fields):
        
        # Creates and saves a staffuser using credentials below
        other_fields.setdefault('is_staff', True)

        staff_user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            department=department,
            **other_fields
        )

        return staff_user
    
    def create_admin(self, email, first_name, last_name, department, password=None, **other_fields):
        # Creates and saves a staffuser using credentials below
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)

        admin_user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            department=department,
            **other_fields
        )

        return admin_user
    
    def create_superuser(self, email, first_name, last_name, department, password=None, **other_fields):
        # Creates and saves a superuser using credentials below
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)

        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            department=department,
            **other_fields
        )

        return user
        
class MyUser(AbstractBaseUser, PermissionsMixin):
    DEPARTMENT_CHOICES = (
        ("CLIENT", "Client"),
        ("EMPLOYEE", "Employee"),
        ("CONTRACTOR", "Contractor"),
        ("SALES", "Sales"),
        ("WAREHOUSE", "Warehouse"),
        ("QUALITY_CONTROL", "QualityControl"),
        ("ACCOUNTING", "Accounting"),
        ("UPPER_MANAGEMENT", "UpperManagement"),
        ("BOARD_MEMBER", "BoardMember")
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(default=timezone.now)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, default="")
    is_client = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin  = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department']

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.email)
    
class Organization(models.Model):
    company = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    is_subscribed = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    subscribed_date = models.DateField(default="", blank=True, null=True)
    unsubscribed_date = models.DateField(default="", blank=True, null=True)
    members = models.ManyToManyField(MyUser)

    def __str__(self):
        return str(self.company)