from django.shortcuts import render
from rest_framework import viewsets, generics, views  # Importing rest framework views, las generics son las que se usan en el mundo real son mas flexibles

# Importing Models
from vet.models import PetOwner, Pet, PetDate
# Importing Serializers previously created
from .serializers import (
                          OwnersSerializers,
                          PetsSerializers,
                          PetsDateSerializers,
                          OwnersListSerializer,
                          Ownerserializer,
                          ContactUserSerializer
                          )


# Create your views here.
                                                            #VIEWS SETS - No so commonly used
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



                                                #GENERIC SETS - Commonly Used

# Respetar la sintaxis  ListModeloAPIView
# Con esta vista, solo se enlistan los owners
class ListOwnersAPIView(generics.ListAPIView):
    """List Owners Api View"""

    queryset = PetOwner.objects.all().order_by("created_at")
    # Llamamos el serializador
    serializer_class = OwnersListSerializer


# Respetar la sintaxis  RetrieveModeloAPIView
# Con esta vista, solo se muestra un owner
class RetrieveOwnersAPIView(generics.RetrieveAPIView):
    """List Owners Api View"""

    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer


class CreateOwnersAPIView(generics.CreateAPIView):
    """Create Owners Api View"""

    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer



class UpdateOwnersAPIView(generics.UpdateAPIView):
    """Update Owners Api View"""

    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer



class DeleteOwnersAPIView(generics.DestroyAPIView):
    """Delete Owners Api View"""

    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer


                                                    #COMBINED API VIEWS

class ListCreateOwnersAPIView(generics.ListCreateAPIView):
    """List Create Owners Api View"""
    queryset = PetOwner.objects.all().order_by("created_at")
    # Llamamos el serializador
    serializer_class = Ownerserializer



class RetrieveUpdateOwnersAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve Update Owners Api View"""
    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer


class RetrieveDestroyOwnersAPIView(generics.RetrieveDestroyAPIView):
    """Retrieve Destroy Owners Api View"""
    queryset = PetOwner.objects.all()
    # Llamamos el serializador
    serializer_class = Ownerserializer

# Class using custom serializer
class ContacUsAPIView(views.APIView):
    """"""
    serializer_class = ContactUserSerializer  # Passing serializer
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)  # Using Custom serializer that does not validate models.
        serializer.is_valid(raise_exception=True)  # Validating each field
        email_instance = serializer.save() # If no exceptions, execute save()
        email_instance.send()    # After accessing POST methods and checkin data , the message proceed to be sent

        return views.Response({"response" : "Email Sent"})  # Return a viewclear

