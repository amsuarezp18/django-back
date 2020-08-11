from rest_framework import serializers
from .models import Delivery, Deliverer

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('x_delivery', 'y_delivery')

class DelivererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliverer
        fields = ('identifier', 'x_deliverer', 'y_deliverer', 'last_updated')