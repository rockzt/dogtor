from rest_framework import serializers # Importing Serializer lonked to the model

from django.core.mail import send_mail # send mail function
from django.conf import settings


# Models
from vet.models import PetOwner, Pet, PetDate # Importing Model


                                                # VIEWS SET SERIALIZERS
# Http -> body
# Serializers -> Representing our API
# serializers.HyperlinkedModelSerializer when model has no relations
# serializers.ModelSerializer when model has relations with other models (1 - N, 1 - 1, N - N)
class OwnersSerializers(serializers.HyperlinkedModelSerializer):
    """Pet Owners serializers"""
    # Considerar que el modelo que se usa posee una foreign key
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

class PetsSerializers(serializers.HyperlinkedModelSerializer):
    """Pet's serializers"""
    # Considerar que el modelo que se usa posee una foreign key
    # La query set contiene los datos del modelo al que se relaciona
    owner = serializers.PrimaryKeyRelatedField(queryset=PetOwner.objects.all(), many=False) # Se pone False debido a que no es una relación many to many, es many to one, owner lo trae como id
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "type",
            "owner",
            "created_at"
        ]

class PetsDateSerializers(serializers.HyperlinkedModelSerializer):
    """PetDate's serializers"""
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all(),
                                               many=False)  # Se pone False debido a que no es una relación many to many, es many to one, pet lo trae como id
    class Meta:
        model = PetDate
        fields = [
            "id",
            "datetime",
            "type",
            "pet",
            "created_at"
        ]

                                                    #GENERIC VIEWS SERIALIZERS

class OwnersListSerializer(serializers.ModelSerializer):
    """Serializer to list alll Pet Owners."""

    class Meta:
        model = PetOwner
        fields = ["id" , "first_name", "last_name", "email"]  # Fields to be displayed


class Ownerserializer(serializers.ModelSerializer):
    """Serializer for detail Pet Owner."""

    class Meta:
        model = PetOwner
        fields = "__all__"  # Display all fields



# Custom class used on ConactUserSerializer()
class Email:
    def __init__(self, to_email, from_email, message, subject, file=None):
        self.to_email = to_email
        self.from_email = from_email
        self.message = message
        self.subject = subject
        self.file = file
    def send(self):
        """Send an Email"""
        send_mail(
            self.subject,
            self.message,
            self.from_email,
            [self.to_email],
            self.file,
        )

class ContactUserSerializer(serializers.Serializer):
    """Contact Form serializer to send a contact email"""

    # Validating data
    subject = serializers.CharField(max_length=10, min_length=5)
    from_email = serializers.EmailField()
    message = serializers.CharField(min_length=20)
    file = serializers.FileField(required=False)


    def create(self, validated_data):
        """Send email"""
        return Email(to_email="rodrigoztrejo@gmail.com", **validated_data)

