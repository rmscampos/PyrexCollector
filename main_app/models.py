from django.db import models


class Pyrex(models.Model):
    pattern = models.CharField(max_length=100)
    shape = models.CharField(max_length=100)
    year = models.IntegerField()
    origin = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.pattern} ({self.id})'

    
