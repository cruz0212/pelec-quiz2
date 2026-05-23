from django.db import models


class EventRegistration(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.full_name} ({self.email})'
