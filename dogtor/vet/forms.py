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
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                }),
            'last_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                }),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'type': 'email',
                }),
            'phone': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                }),
        }




class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "type", "owner"]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                }),
            'type': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                }),
            'owner': forms.Select(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                }),
        }


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


class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=50, required=False, label='Search')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        # Add attributes to the search_query field
        self.fields['search_query'].widget.attrs.update({
            'class': 'form-control me-2r',
            'type': 'search',
            'placeholder': 'Enter a name...',
        })
