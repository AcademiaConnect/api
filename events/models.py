from django.db import models
from django.contrib.auth.models import User


class Events(models.Model):
    title = models.CharField(max_length=150)
    dateInitial = models.DateTimeField()
    dateFinal = models.DateTimeField()
    location = models.CharField(max_length=150)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
