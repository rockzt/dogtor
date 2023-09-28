from django.urls import path, include
from rest_framework import routers  # Importing routers from res_framework
# Importing Views
# from .views import  OwnersViewSet, PetsViewSet, PetsDateViewSet importing view sets
from .views import ListOwnersAPIView, RetrieveOwnersAPIView, CreateOwnersAPIView, UpdateOwnersAPIView, DeleteOwnersAPIView, ListCreateOwnersAPIView, RetrieveUpdateOwnersAPIView, RetrieveDestroyOwnersAPIView, ContacUsAPIView



# Router when using View Sets
# router = routers.DefaultRouter() # Creating router
# router.register(r"owners", OwnersViewSet)   # Registering router for Owners (r"resource", viewName)
# router.register(r"pets", PetsViewSet)   # Registering router  (r"pets", viewName)
# router.register(r"petsdate", PetsDateViewSet)   # Registering router  (r"petsdate", viewName)


urlpatterns = [
    # path("", include(router.urls))  # Setting router on urls when using view sets
      path("owners/list", ListOwnersAPIView.as_view(), name="owners_list"),
      path("owners/<int:pk>/detail", RetrieveOwnersAPIView.as_view(), name="owners_detail"),
      path("owners/add/", CreateOwnersAPIView.as_view(), name="owners_create"),
      path("owners/<int:pk>/update/", UpdateOwnersAPIView.as_view(), name="owners_update"),
      path("owners/<int:pk>/destroy/", DeleteOwnersAPIView.as_view(), name="owners_destroy"),
      # Combined APIViews, according restful pattern
      path("owners/", ListCreateOwnersAPIView.as_view(), name="owners_list_create"),
      path("owners/<int:pk>/", RetrieveUpdateOwnersAPIView.as_view(), name="owners_retrieve_update"),
      path("owners/<int:pk>/delete/", RetrieveDestroyOwnersAPIView.as_view(), name="owners_retrieve_destroy"),

      # URL using custom serializer to send email
      path("conact-us/", ContacUsAPIView.as_view(), name="contact_us_email")
]

# CREATE OWNER -> CreateAPIView
# UPDATE OWNER -> UpdateAPIView
# DELETE OWNER -> DestroyAPIView

# TAREA -> trasnformar a API REST usando otras vistas, investigar generics - OK