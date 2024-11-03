from django.db import models



class Location(models.Model):
    name = models.CharField(max_length=50)
    UserId = models.ForeignKey('users.User', on_delete=models.CASCADE)
    Latitude = models.DecimalField(max_digits=4, decimal_places=2)
    Longitude = models.DecimalField(max_digits=4, decimal_places=2)

