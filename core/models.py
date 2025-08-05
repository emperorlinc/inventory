from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveIntegerField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(upload_to="img", blank=True, null=True)

    def __str__(self) -> str:
        return self.user.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


STATUS = (
    ("UP", "Unpaid"),
    ("PP", "Partly paid"),
    ("FP", "Fully paid"),
)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    catergory = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="product_created_by", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, related_name="product_updated_by", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    Distributor_contact = models.CharField(max_length=15)
    delivery_date = models.DurationField()
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=STATUS, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_quantity = models.PositiveSmallIntegerField(
        blank=True, null=True)
    catergory = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="order_created_by", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, related_name="order_updated_by", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self) -> str:
        return self.product.name

    @property
    def total_func(self):
        return self.price * self.quantity

    @property
    def balance_func(self):
        return self.total_amount - self.amount_paid

    @property
    def total_quantity_func(self):
        self.total_quantity = self.quantity
        return self.total_quantity


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="sale_created_by", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, related_name="sale_updated_by", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    @property
    def total_func(self):
        return self.price * self.quantity

    @property
    def balance_func(self):
        return self.total_amount - self.price

    @property
    def quantity_func(self):
        return self.product.quantity - self.quantity

    def __str__(self) -> str:
        return self.product.name
