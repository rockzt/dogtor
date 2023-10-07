from django.urls import path
# Views            function view|          Class view|
from .views import (list_pet_owners,
                    Test,
                    OwnersList,
                    Home,
                    OwnersDetail,
                    PetsList,
                    PetsDetail,
                    OwnersCreate,
                    OwnersUpdate,
                    PetsCreate,
                    PetsUpdate,
                    OwnersDelete,
                    PetsDelete,
                    PetdatesList,
                    PetdatesDetial,
                    PetdatesCreate,
                    PetsdatesUpdate,
                    GenerateCSVView
                    )

# alias (reversed urls) -> app's urls in specific
# alias (reversed urls) -> project's routes

# if does not posses include -> reversed url set as third parameter
# otherwise -> reversed url set as second parameter inside INCLUDE passing a tuple
# SINTAXIS
# If you want to access  "vet:owners_list"
urlpatterns = [
    path('', Home.as_view(),name="home"),
    path('owners', OwnersList.as_view(), name="owners_list"), # Configuring generic class view, Listview, renders template, include and alias  "owners_list", this is the sintaxis when you do not posess include
    path('owners/<int:pk>', OwnersDetail.as_view(), name="owners_detail"), # Configuring generic class view, DetailView, renders template, include and alias  "owners_list"
    path('owners/add', OwnersCreate.as_view(), name="owners_create"), # Configuring CreateView of owners
    path('owners/<int:pk>/edit', OwnersUpdate.as_view(), name="owners_edit"), # Configuring UpdateView, setting route using pk to locate what owner we want to edit
    path('owners/<int:pk>/delete', OwnersDelete.as_view(), name="owners_delete"), # Configuring DeleteView, setting route using pk to locate what owner we want to delete
    path('pets/add', PetsCreate.as_view(), name="pets_create"), # Configuring CreateView of Pets
    path('pets/<int:pk>/delete', PetsDelete.as_view(), name="pets_delete"), # Configuring DeleteView, setting route using pk to locate what owner we want to delete
    path('pets/<int:pk>/edit', PetsUpdate.as_view(), name="pets_edit"), # Configuring CreateView of Pets
    path('pets', PetsList.as_view(), name="pets_list"), # Configuring generic class view, renders template
    path('pets/<int:pk>', PetsDetail.as_view(), name="pets_detail"), # Configuring generic class view, renders template
    path('petdates', PetdatesList.as_view(), name="petdates_list"), # Configuring generic class view, renders template
    path('petdates/<int:pk>', PetdatesDetial.as_view(), name="petdates_detail"), # Configuring generic class view, renders template
    path('petdates/add', PetdatesCreate.as_view(), name="petdates_create"), # Configuring CreateView of Petdates
    path('petdates/<int:pk>/edit', PetsdatesUpdate.as_view(), name="petdates_edit"), # Configuring CreateView of Petdates
    # Simple Views
    path('test', Test.as_view()), # Configuring generic class view, this class does not render template
    path('generate-csv/', GenerateCSVView.as_view(), name='generate_csv'),
]
