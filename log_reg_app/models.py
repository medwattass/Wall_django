from django.db import models
import bcrypt, re
from django.utils import timezone
from datetime import datetime


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        email = postData.get('email')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if User.objects.filter(email=email).exists():
            errors["email"] = "This email have been already used"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['first_name']) < 3:
            errors["first_name"] = "First name should be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Last name should be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirmation']:
            errors["password_confirmation"] = "Password doesn't match!"
        birthday_str = postData.get('birthday')
        if birthday_str:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            current_date = timezone.now().date()
            if birthday > current_date:
                errors["past_date"] = "Birthday must be in the past"
            else:
                age = calculate_age(birthday, current_date)
                if age < 13:
                    errors["birthday"] = "You must be at least 13 years old"
        
        return errors
    
    def validator_pwd(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors["password"] = "Incorrect email/password"
        else:
            errors["no_user"] = "No user registred with this email"
        return errors


def calculate_age(birthday, current_date):
    age = current_date.year - birthday.year
    if current_date.month < birthday.month or (current_date.month == birthday.month and current_date.day < birthday.day):
        age -= 1
    return age

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
