from django.shortcuts import render
from rest_framework import viewsets  # Importing rest framework views

# Importing Models
from vet.models import PetOwner, Pet, PetDate
# Importing Serializers previously created
from .serializers import OwnersSerializers, PetsSerializers, PetsDateSerializers


# Create your views here.

# Contains LIST, RETRIEVE, UPDATE, CREATE, DELETE
class OwnersViewSet(viewsets.ModelViewSet):
    """ViewSet PetOwner's Mpdel"""
    # 1.- queryset to be apply -> ORM
    # 2.- Serializer

    # Get all owners -> PetOwner.objects.all()
    queryset = PetOwner.objects.all()
    serializer_class = OwnersSerializers  # Using serializer on our view


class PetsViewSet(viewsets.ModelViewSet):
    """ViewSet Pet's Mpdel"""


    queryset = Pet.objects.all()
    serializer_class = PetsSerializers




class PetsDateViewSet(viewsets.ModelViewSet):
    """ViewSet Pet's Mpdel"""


    queryset = PetDate.objects.all()
    serializer_class = PetsDateSerializers
