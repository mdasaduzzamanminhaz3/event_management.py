from django.db import models

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

    def __str__(self):
        return self.name
    


class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField('Event',related_name='participants')

    def __str__(self):
        return self.name
    


