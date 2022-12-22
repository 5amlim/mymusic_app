from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

OCCASION = (
    ('D', 'Driving'),
    ('S', 'Studying'),
    ('L', 'Leisure')
)
class Artist(models.Model):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('artists_detail', kwargs={'pk': self.id})

# Create your models here.
class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ManyToManyField(Artist, related_name= 'songs')
    album = models.TextField(max_length=250)
    release_date = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'song_id': self.id})
    
    def popular_today(self):
        print(f'🪲 {date.today()}')
        return self.session_set.filter(date=date.today()).count() >= 5


class Session(models.Model):
    date = models.DateField()
    occasion = models.CharField(max_length=1, choices=OCCASION, default=OCCASION[0][0])
        
    song = models.ForeignKey(Music, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_occasion_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']

