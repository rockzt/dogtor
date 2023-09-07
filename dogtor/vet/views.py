from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import View, TemplateView  # Impoting TemplateView for generic class view
# Models
from vet.models import PetOwner


# Create your views here.
def list_pet_owners(request):
    # Por defualt, esta visya usa el método GET
    print(request.__dict__)
    """List owners."""
    owners = PetOwner.objects.all()
    context = {
        "owners" : owners,
    }

    template = loader.get_template("vet/owners/list.html")
    return HttpResponse(template.render(context, request))

# Render template
class OwnersList(TemplateView):
    # Rendering template
    template_name = "vet/owners/list.html"
    # Passing context, overwriting class to pass context
    def get_context_data(self, **kwargs):
        # Catching inherited context by TemplateView class
        context  = super().get_context_data(**kwargs)
        # Adding our custom context, retrieving data from our DB
        context["owners"] = PetOwner.objects.all()
        # Returning context
        return context

# Render text
class Test(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("Hello there, from generic class view!!!")

