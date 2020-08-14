from .models import Deliverer, Delivery
from .serializers import DeliverySerializer, DelivererSerializer, DeliverySerializerSent, Testing
from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
import math
import requests

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
            print(serializer.data)
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

@api_view(['GET'])
def UpdateData(request):
    response = requests.get('https://gist.githubusercontent.com/CesarF/24a0d07afa64532a0ee72b32f554ed8f/raw/ae28ea0e1f9eb4e143d96fe932731d24763beb92/points.json')
    data = response.json()
    for i in range(len(data)):
        dict_simp = {"identifier":data[i]["id"],"x_deliverer":data[i]["x"],"y_deliverer":data[i]["y"]}
        serializer = Testing(data=dict_simp)
        if serializer.is_valid():
            id_new = serializer.data['identifier']
            point_to_edit = get_object_or_404(Deliverer, identifier=id_new)
            point_to_edit.x_deliverer = serializer.data['x_deliverer']
            point_to_edit.y_deliverer = serializer.data['y_deliverer']
            point_to_edit.last_updated =datetime.now()
            point_to_edit.save()

    snippets = Deliverer.objects.all()
    serializer = DelivererSerializer(snippets, many=True)
    return Response(serializer.data)