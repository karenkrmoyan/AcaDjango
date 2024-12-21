from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500, null=True, blank=True)
    rating = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)

    def average_rating(self, new_rating):
        self.rating = (self.rating * self.vote_count + int(new_rating)) / (self.vote_count + 1)
        self.rating = round(self.rating, 2)
        self.vote_count += 1
        self.save()


class Lecture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)

