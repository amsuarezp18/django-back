from django.db import models

class Delivery(models.Model):
    identifier = models.PositiveIntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    last_update = models.DateField()

