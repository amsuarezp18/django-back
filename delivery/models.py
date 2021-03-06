from django.db import models

class Deliverer(models.Model):
    identifier = models.PositiveIntegerField()
    x_deliverer = models.IntegerField()
    y_deliverer = models.IntegerField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.identifier)

class Delivery(models.Model):
    x_delivery = models.IntegerField()
    y_delivery = models.IntegerField()
    deliverer = models.ForeignKey(Deliverer,on_delete=models.CASCADE,related_name='delivery_deliverer')

