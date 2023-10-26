from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserEditForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from urllib.parse import parse_qs
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages




# Create your views here.

def registration_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #email = get_email(request)
            #print(register_mail(email))  # This will print the email address
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
            messages.success(request, 'User Info Updated successfully.')
            return redirect('/account/edit_profile/')  # Redirect to the user's profile page
        else:
            messages.error(request, 'Something went wrong updating user info!!!.')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})





def register_mail(user_email):
    # Send the welcome email
    subject = 'Welcome to Our Website'
    message = 'Thank you for registering on our website!'
    from_email = 'your-email@example.com'
    recipient_list = [user_email]

    # Load the HTML email template
    #html_message = render_to_string('welcome_email.html', {})

    # Send the email
    output = send_mail(subject, message, from_email, recipient_list, html_message=f'Hello there! {user_email}', fail_silently=False,)
    return output


def get_email(request):
    # Assuming request.body contains the form data as bytes
    form_data = request.body.decode('utf-8')
    # Parse the URL-encoded form data
    form_data_dict = parse_qs(form_data)
    # Get the email value from the form data
    email = form_data_dict.get('email', [''])[0]
    # Decode the email address (if needed)
    email = email.replace('%40', '@')  # Replace %40 with @ if present
    return email
