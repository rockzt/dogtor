from django.contrib import admin
from . import models
# Register your models here.

class VetAdminArea(admin.AdminSite):
    """Blog admin panel administration."""

    site_header = "Vet Site Admin Area"


# Instancing our class to use it.
vet_admin_site = VetAdminArea(name="VetAdmin") # The passing argument its representative and it is not important which name you give it

# Registering models from our models.py on blog model
vet_admin_site.register(models.PetOwner)
vet_admin_site.register(models.Pet)
vet_admin_site.register(models.PetDate)

# Registering on the general admin panel
admin.site.register(models.PetOwner)
admin.site.register(models.Pet)
admin.site.register(models.PetDate)
