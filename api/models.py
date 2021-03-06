from django.db import models
from django.db.models.deletion import CASCADE
# Import built in django auth users. Can be seen in admin/ page
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def number_of_ratings(self):
        # Get all ratings for current movie
        # Rating. is valid as Rating class is linked via ForeignKey below
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)
    
    def average_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        if len(ratings) > 0:
            for x in ratings:
                sum += x.stars
            return sum / len(ratings)
        else:
            return sum

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),
MaxValueValidator(5)])
    
    class Meta:
        # Do not allow the same user to rate a movie multiple times.
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)