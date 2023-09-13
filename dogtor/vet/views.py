from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import View, TemplateView, ListView, DetailView  # Importing TemplateView for generic class view
# Models
from vet.models import PetOwner, Pet


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
'''
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
'''

class OwnersList(ListView):
    # 1.- Use model we want to use.
    # 2.- Pass template to render.
    # 3.- Pass the context with the data we want to manipulate.
    model = PetOwner # 1 Model
    template_name = 'vet/owners/list.html' # 2 Template
    context_object_name = "owners" # 3 Context

class OwnersDetail(DetailView):
    """Renders a specific Pet Owner with their pk"""
    # 1. Modelo
    # 2. Template to create
    # 3. Context to use on the template
    model = PetOwner
    template_name = 'vet/owners/detail.html'
    context_object_name = "owner"

class PetsList(ListView):
    # Rendering template

    model = Pet  # 1 Model
    print(model)
    template_name = "vet/pets/list.html"  # 2 Template
    context_object_name = "pets"  # 3 Context

class PetDetail(DetailView):
    # Rendering template

    model = Pet
    print(model)
    template_name = "vet/pets/detail.html"
    context_object_name = "pet"

'''
      USING TEMPLATE VIEW
class PetsList(TemplateView):
    # Rendering template
    template_name = "vet/pets/list.html"

    # Passing context, overwriting class to pass context
    def get_context_data(self, **kwargs):
        # Catching inherited context by TemplateView class
        context = super().get_context_data(**kwargs)
        # Adding our custom context, retrieving data from our DB
        try:
            context["pets"] = Pet.objects.all()
        except Pet.DoesNotExist:
            context["pets"] = []
        # Returning context
        return context

class PetDetail(TemplateView):
    # Rendering template
    template_name = "vet/pets/detail.html"

    # Passing context, overwriting class to pass context
    def get_context_data(self, **kwargs):
        # Catching inherited context by TemplateView class
        context = super().get_context_data(**kwargs)
        # Adding our custom context, retrieving data from our DB
        try:
            context["pet"] = Pet.objects.get(pk=self.kwargs['pk'])
        except Pet.DoesNotExist:
            context["pet"] = ""
        # Returning context
        return context
'''

# Render text
class Test(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("Hello there, from generic class view!!!")



class Welcome(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("<div style='text-align:center;'><h1>Welcome to Vet App!!!</h1><div>")

