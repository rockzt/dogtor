from rest_framework import serializers # Importing Serializer lonked to the model

# Models
from vet.models import PetOwner, Pet, PetDate # Importing Model

# Serializers -> Representing our API
# serializers.HyperlinkedModelSerializer when model has no relations
# serializers.ModelSerializer when model has relations with other models (1 - N, 1 - 1, N - N)
class OwnersSerializers(serializers.HyperlinkedModelSerializer):
    """Pet Owners serializers"""

    class Meta:
        model = PetOwner # Model
        # Model's Fields
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone",
            "created_at"
        ]

class PetsSerializers(serializers.ModelSerializer):
    """Pet's serializers"""

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "type",
            "owner",
            "created_at"
        ]

class PetsDateSerializers(serializers.ModelSerializer):
    """PetDate's serializers"""

    class Meta:
        model = PetDate
        fields = [
            "id",
            "datetime",
            "type",
            "pet",
            "created_at"
        ]