from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('x', 'y')

class DeliverySerializerTwo(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ('identifier', 'x', 'y', 'last_update')