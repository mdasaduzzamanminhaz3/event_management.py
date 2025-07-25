from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def profile_image_path(instance, filename):
    return f'profile_images/{instance.username}/{filename}'

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to=profile_image_path,blank=True,null=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username
