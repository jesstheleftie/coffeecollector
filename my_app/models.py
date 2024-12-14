from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

RATINGS = (
    ('1', '1 Star'),
    ('2', '2 Stars'),
    ('3', '3 Stars'),
    ('4', '4 Stars'),
    ('5', '5 Stars')
)

class Coffee(models.Model):
    name = models.CharField(max_length=100)
    roast = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    roast_age_in_months = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Use the 'reverse' function to dynamically find the URL for viewing this cat's details
        return reverse('coffee-detail', kwargs={'coffee_id': self.id})



class Rating(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    # date = models.DateField('Rating Date')
    rating = models.CharField(max_length=1,
    choices =RATINGS,
    default=RATINGS[0][0])
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_rating_display()} on {self.date}"
    
    # Define the default order of feedings
    class Meta:
        ordering = ['-date']  # This line makes the newest feedings appear first
