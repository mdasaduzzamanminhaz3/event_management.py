from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rsvp_event')
    asset = models.ImageField(upload_to='event_asset',blank=True,null=True,default="event_asset/default_img.jpg")
    def __str__(self):
        return self.name
    




