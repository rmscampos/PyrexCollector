from django.db import models
from django.urls import reverse




class Food(models.Model):
    dish_name = models.CharField(max_length=100)
    date_made = models.IntegerField()
    chef = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.dish_name
    
    def get_absolute_url(self):
        return reverse('foods_detail', kwargs={'pk': self.id})



class Pyrex(models.Model):
    pattern = models.CharField(max_length=100)
    shape = models.CharField(max_length=100)
    year = models.IntegerField()
    origin = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pattern} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pyrex_id': self.id})
    
