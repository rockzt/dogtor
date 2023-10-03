from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.

def registration_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/registration_form.html", {"form": form})