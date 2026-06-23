from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        data = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invaild Email Address!"
        if len(data) > 0:
            errors['email'] = "Email already exists!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Passwords don't match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        email = postData['email']
        password = postData['password']
        data = User.objects.filter(email=email)
        if len(email) < 1:
            errors["email"] = "Email cannot be empty!"
        elif not EMAIL_REGEX.match(email):
            errors["email"] = "Invalid Email Address!"
        elif len(data) == 0:
            errors["email"] = "Email does not exist. Register first!"
        elif not bcrypt.checkpw(password.encode(), data[0].password.encode()):
            errors["password"] = "Incorrect password. Try again!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    rewards = models.IntegerField(default=0)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    food_name = models.CharField(max_length=45)
    desc = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, related_name="items", on_delete=models.CASCADE, blank=True, null=True)


class UserItem(models.Model):
    food_name = models.CharField(max_length=45)
    desc = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    points = models.IntegerField()
    category = models.ForeignKey(Category, related_name="user_items", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="items", on_delete=models.CASCADE, blank=True, null=True)

