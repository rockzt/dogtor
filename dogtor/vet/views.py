from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin  # Importing permissions for views and login required
from django.views.generic import (View,
                                  TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView
                                  ) # Importing TemplateView for generic class view
from .forms import OwnerForm, PetForm# Importing forms that will be used on views
from django.urls import reverse_lazy  # Importing to use reversed urls
# Models
from vet.models import PetOwner, Pet, PetDate
# Handling Errors on Delete View
from django.db.models import ProtectedError
from django.shortcuts import render


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
    paginate_by = 6  # Pagination parameter, how many records you want to show per page -> 1
    ordering = 'created_at'  # Sorting results

class OwnersDetail(LoginRequiredMixin ,DetailView):  # When inheriting from LoginRequiredMixin, you must be logged to access this view
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
    template_name = "vet/pets/list.html"  # 2 Template
    context_object_name = "pets"  # 3 Context
    paginate_by = 6  # Pagination parameter, how many records you want to show per page -> 1
    ordering = 'created_at' # Sorting results

class PetsDetail(DetailView):
    # Rendering template

    model = Pet
    template_name = "vet/pets/detail.html"
    context_object_name = "pet"


class PetdatesList(ListView):
    model = PetDate
    template_name = "vet/petdates/list.html"
    context_object_name = "petdates"
    paginate_by = 6
    ordering = 'created_at'

class PetdatesDetial(DetailView):
    model = PetDate
    template_name = "vet/petdates/detail.html"
    context_object_name = "petdate"


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
class OwnersCreate(CreateView):
    """View used to create PetOwner"""
    # 1.- Model
    # 2.- Template to render
    # 3.- Form it's going to be created with
    # 4.- The url if the request was successful and will be redirected to this-> reversed url

    model = PetOwner # 1
    template_name = "vet/owners/create.html" # 2
    form_class = OwnerForm # 3
    success_url = reverse_lazy('vet:owners_list') # 4


class OwnersUpdate(PermissionRequiredMixin ,UpdateView):
    """View used to update a PetOwner"""
    # Permission required to access this view
    # app.action_mode
    permission_required = "vet.change_petowner" #app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/admin/login"  # redirect url in case you are not logged, this urls redirect you to the login admin panel
    redirect_field_name = "next" # related to query param

    model = PetOwner
    template_name = "vet/owners/update.html"
    form_class = OwnerForm # If you want to update specific fields, you can create another form  in forms.py with specific fields

    success_url = reverse_lazy('vet:owners_list')  # 4


class PetsCreate(CreateView):
    """View used to create Pet"""

    model = Pet # 1
    template_name = "vet/pets/create.html" # 2
    form_class = PetForm # 3
    success_url = reverse_lazy('vet:pets_list') # 4


class PetsUpdate(UpdateView):
    """View used to update a PetOwner"""
    model = Pet
    template_name =  "vet/pets/update.html"
    form_class = PetForm # If you want to update specific fields, you can create another form  in forms.py with specific fields

    success_url = reverse_lazy('vet:pets_list')  # 4

class OwnersDelete(DeleteView):
    model = PetOwner
    template_name = "vet/owners/delete.html"
    success_url = reverse_lazy('vet:owners_list')

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            # Customize the error message
            error_message = f"Cannot delete owner, has at least one pet related. ({e})"
            res = str(e).split(', ')
            pet_pk_str = res[3].replace('>', '').replace('}', '').replace(')', '')
            pk_user = kwargs['pk']
            pet_pk = int(pet_pk_str)
            owner_error = PetOwner.objects.get(pk=pk_user)
            return render(request, 'vet/owners/delete.html', {'error_message': error_message, 'owner_error': owner_error, 'pet_pk' : pet_pk})


class PetsDelete(DeleteView):
    model = Pet
    template_name = "vet/pets/delete.html"
    success_url = reverse_lazy('vet:pets_list')

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            # Customize the error message
            error_message = f"Cannot delete pet -> ({e})"
            # res = str(e).split(', ')
            # pet_pk_str = res[3].replace('>', '').replace('}', '').replace(')', '')
            # pk_user = kwargs['pk']
            # pet_pk = int(pet_pk_str)
            # owner_error = PetOwner.objects.get(pk=pk_user)
            return render(request, 'vet/owners/delete.html', {'error_message': error_message})


# Render text
class Test(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("Hello there, from generic class view!!!")


''' 
class Welcome(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("<div style='text-align:center;'><h1>Welcome to Vet App!!!</h1><div>")
'''

class Home(TemplateView):
    # Rendering template
    template_name = "vet/home.html"

    # Passing context, overwriting class to pass context
    def get_context_data(self, **kwargs):
        # Catching inherited context by TemplateView class
        context = super().get_context_data(**kwargs)
        # Adding our custom context, retrieving data from our DB
        try:
            context["pets_count"] = Pet.objects.count()
        except Pet.DoesNotExist:
            context["pets_count"] = 0

        try:
            context["owners_count"] = PetOwner.objects.count()
        except PetOwner.DoesNotExist:
            context["owners_count"] = 0

        try:
            context["pet_date_count"] = PetDate.objects.count()
        except PetDate.DoesNotExist:
            context["pet_date_count"] = 0

        try:
            context["pet_last_created"] = Pet.objects.last()
        except PetDate.DoesNotExist:
            context["pet_last_created"] = ""

        try:
            context["pet_owner_last_created"] = PetOwner.objects.last()
        except PetDate.DoesNotExist:
            context["pet_owner_date_count"] = ""

        try:
            context["pet_date_last_created"] = PetDate.objects.last()
        except PetDate.DoesNotExist:
            context["pet_date_last_created"] = ""

        # Returning context
        return context

# Customized Error Views
def error_404(request, exception):
    return render(request, 'vet/404.html')

def error_403(request, exception):
    return render(request, 'vet/403.html')