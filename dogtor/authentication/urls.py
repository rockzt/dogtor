from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    # Add other URL patterns as needed
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]