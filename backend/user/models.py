# users/models.py
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Avg

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True)

    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class InstructorProfile(models.Model):
    profile_pics = models.ImageField(
        default='default.png', upload_to='profile_pics')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_name = models.CharField(
        max_length=255, default='', null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class StudentProfile(models.Model):
    profile_pics = models.ImageField(
        default='default.png', upload_to='profile_pics')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Course(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255)
    what_you_learn = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    targeted_audience = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="courses")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    duration_in_hours = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at', 'updated_at']

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def get_student_purchased_count(self):
        return Cartitems.objects.filter(course=self, cart__completed=True).count()
    
    def get_average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    def get_what_you_learn_list(self):
        return self.what_you_learn.split('\n')

    def get_requirements_list(self):
        return self.requirements.split('\n')
    
    def get_targeted_audience_list(self):
        return self.targeted_audience.split('\n')


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Cart"


class Cartitems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')

    def __str__(self):
        return f"{self.cart.user.username} items"


class WatchList(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} WatchList"


class Watchitems(models.Model):
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cart.user.username} items"


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user} reviewed {self.course}"


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
