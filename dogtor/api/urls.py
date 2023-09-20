from django.urls import path, include
from rest_framework import routers  # Importing routers from res_framework
# Importing Views
from .views import  OwnersViewSet, PetsViewSet, PetsDateViewSet

# Router
router = routers.DefaultRouter() # Creating router
router.register(r"owners", OwnersViewSet)   # Registering router for Owners (r"resource", viewName)
router.register(r"pets", PetsViewSet)   # Registering router  (r"pets", viewName)
router.register(r"petsdate", PetsDateViewSet)   # Registering router  (r"petsdate", viewName)


urlpatterns = [
    path("", include(router.urls))  # Setting router on urls
]