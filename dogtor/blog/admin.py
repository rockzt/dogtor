from django.contrib import admin

# Importing Models
from . import models # Importing all models

# Register your models here.

# Improved way to create a model admin that specify which fields can be shown on admin site
@admin.register(models.Post)   # Registering Models and Passing Custom Model
class PostAdmin(admin.ModelAdmin):
    """Post Admin model for admin"""
    fields = ["name"]



# Site -> Admin panel for blog app
class BlogAdminArea(admin.AdminSite):
    """Blog admin panel administration."""

    site_header = "Blog Site Admin Area"


# Instancing our class to use it.
blog_admin_site = BlogAdminArea(name="BlogAdmin") # The passing argument its representative and it is not important which name you give it


       # Old Way Registering Models

# Registering on the general admin panel
# blog_admin_site.register(models.Post, PostAdmin)
# admin.site.register(models.Post, PostAdmin)