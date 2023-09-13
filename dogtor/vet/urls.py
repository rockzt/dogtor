from django.urls import path
# Views            function view|          Class view|
from .views import list_pet_owners, Test, OwnersList, Welcome, OwnersDetail, PetsList, PetDetail, OwnersCreate, OwnersUpdate

# alias (reversed urls) -> app's urls in specific
# alias (reversed urls) -> project's routes

# if does not posses include -> reversed url set as third parameter
# otherwise -> reversed url set as second parameter inside INCLUDE passing a tuple
# SINTAXIS
# If you want to access  "vet:owners_list"
urlpatterns = [
    path('', Welcome.as_view()),
    path('owners/', OwnersList.as_view(), name="owners_list"), # Configuring generic class view, Listview, renders template, include and alias  "owners_list", this is the sintaxis when you do not posess include
    path('owners/<int:pk>', OwnersDetail.as_view(), name="owners_detail"), # Configuring generic class view, DetailView, renders template, include and alias  "owners_list"
    path('owners/add/', OwnersCreate.as_view(), name="owners_create"), # Configuring CreateView
    path('owners/<int:pk>/edit/', OwnersUpdate.as_view(), name="owners_edit"), # Configuring UpdateView, setting route using pk to locate what owner we want to edit
    path('pets/', PetsList.as_view(), name="pets_list"), # Configuring generic class view, renders template
    path('pets/<int:pk>', PetDetail.as_view(), name="pets_detail"), # Configuring generic class view, renders template
    path('test/', Test.as_view()), # Configuring generic class view, this class does not render template
]
