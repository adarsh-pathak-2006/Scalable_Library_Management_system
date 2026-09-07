from django.db import models
from django.contrib.auth.models import AbstractUser

class College(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    code=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES=[('LIBRARIAN', 'Librarian'), ('STUDENT', 'Student')]

    role=models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    mobile_no=models.CharField(max_length=15, unique=True, null=False, blank=False)  
    college=models.ForeignKey(College, on_delete=models.CASCADE, null=False, blank=False)  

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='pfps/', null=True)
    roll_no=models.CharField(max_length=15)

    def __str__(self):
        return self.user.username


