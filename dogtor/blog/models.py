from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True, null=True)
    # blank -> form/django
    # null -> data base

    def __str__(self):
        return f"{self.pk} :{self.name}"