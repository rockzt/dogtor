from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


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




def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/edit_profile/')  # Redirect to the user's profile page
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})