from .models import Delivery
from .serializers import DeliverySerializer, DeliverySerializerTwo
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import math
import json

class LeadListCreate(generics.ListCreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

@api_view(["POST"])
def ClosestPoint(request):
    try:
        response = request.data
        serializer = DeliverySerializer(data=response)
        if serializer.is_valid():
            coord_x = serializer.data['x']
            coord_y = serializer.data['y']
            list = Delivery.objects.all()
            return_data = select_nearest_neighbor(coord_x, coord_y, list)
            serializer = DeliverySerializerTwo(return_data)
        return Response(serializer.data)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def select_nearest_neighbor(starting_point_x, starting_point_y, neighbors):
    if len(neighbors) == 1:
        return neighbors[0]
    else:
        nearest_neighbor = None
        nearest_distance = None
        for item in neighbors:
            if not nearest_neighbor:
                nearest_neighbor = item
                nearest_distance = math.sqrt(((item.x-starting_point_x)**2)+((starting_point_y)**2))
            else:
                item_distance_to_start_point = math.sqrt(((item.x-starting_point_x)**2)+((starting_point_y)**2))
                if item_distance_to_start_point < nearest_distance:
                    nearest_distance = item_distance_to_start_point
                    nearest_neighbor = item
        return nearest_neighbor
