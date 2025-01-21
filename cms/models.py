from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6)
    ROLE_CHOICES = (('admin', 'Admin'), ('author', 'Author'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='author')

    objects = UserManager()  # Use the custom manager
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    USERNAME_FIELD = 'email'  # Set email as the unique identifier
    REQUIRED_FIELDS = []  # Define additional required fields

    def __str__(self):
        return self.email

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# Content Model
class Content(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    summary = models.CharField(max_length=60)
    document = models.FileField(upload_to='documents/')
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Contents"
