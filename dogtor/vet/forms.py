from django import forms

# Importing models
from .models import PetOwner, Pet, PetDate

# Link forms with models
# Forms -> Classes


class OwnerForm(forms.ModelForm):
    # 1.- Model relate to current form
    # 2.- Fields presented on the current form

    class Meta:
        model = PetOwner # 1
        fields = ["first_name", "last_name", "address", "email", "phone"]

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "type", "owner"]


class PetdateForm(forms.ModelForm):


    class Meta:
        model = PetDate
        fields = ["datetime", "type", "pet"]
        widgets = {
            'datetime': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
            'pet': forms.Select(
                attrs={
                    'class': 'form-control',
                }),
        }