from django.contrib.auth import get_user_model
from django.db import models



class Location(models.Model):
    name = models.CharField(max_length=50)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=4, decimal_places=2)
    longitude = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name