from django import forms

# Importing models
from .models import PetOwner

# Link forms with models
# Forms -> Classes


class OwnerForm(forms.ModelForm):
    # 1.- Model relate to current form
    # 2.- Fields presented on the current form

    class Meta:
        model = PetOwner # 1
        fields = ["first_name", "last_name", "address", "email", "phone"]