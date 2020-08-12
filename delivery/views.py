from .models import Deliverer, Delivery
from .serializers import DeliverySerializer, DelivererSerializer, DeliverySerializerSent
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import math
import json

@api_view(['GET'])
def LeadListCreate(request):
    snippets = Deliverer.objects.all()
    serializer = DelivererSerializer(snippets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def LeadListDelivery(request):
    snippets = Delivery.objects.all()
    serializer = DeliverySerializerSent(snippets, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def ClosestPoint(request):
    try:
        response = request.data
        serializer = DeliverySerializer(data=response)
        if serializer.is_valid():
            coord_x = serializer.data['x_delivery']
            coord_y = serializer.data['y_delivery']
            list = Deliverer.objects.all()
            return_data = select_nearest_neighbor(coord_x, coord_y, list)
            serializer = DelivererSerializer(return_data)
            Delivery.objects.create(x_delivery=coord_x, y_delivery=coord_y,deliverer=return_data)

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
                nearest_distance = math.sqrt(((item.x_deliverer - starting_point_x) ** 2) + ((item.y_deliverer - starting_point_y) ** 2))
            else:
                item_distance_to_start_point = math.sqrt(((item.x_deliverer - starting_point_x) ** 2) + ((item.y_deliverer - starting_point_y) ** 2))
                if item_distance_to_start_point < nearest_distance:
                    nearest_distance = item_distance_to_start_point
                    nearest_neighbor = item
        return nearest_neighbor
