from django.urls import path
# Views
from .views import list_pet_owners, Test, OwnersList

urlpatterns = [
    path('owners/', OwnersList.as_view()), # Configuring generic class view, this class renders a template
    path('test/', Test.as_view()), # Configuring generic class view, this class does not render template
]
