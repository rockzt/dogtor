from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
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
from .forms import OwnerForm, PetForm, PetdateForm, SearchForm# Importing forms that will be used on views
from django.urls import reverse_lazy  # Importing to use reversed urls
# Models
from vet.models import PetOwner, Pet, PetDate
# Handling Errors on Delete View
from django.db.models import ProtectedError
from django.shortcuts import render
import logging   # Use to log actions
from dal import autocomplete # Required for search box on select field
from django.apps import apps
import csv
from ast import literal_eval

logger = logging.getLogger(__name__)


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

class OwnersList(LoginRequiredMixin ,ListView, PermissionRequiredMixin):


    # Permissions Section
    #permission_required = "vet.can_change_pet_date"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    #raise_exception = True  # True -> Raise exception when you do not have permission
    #login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    #redirect_field_name = "next"  # related to query param


    # 1.- Use model we want to use.
    # 2.- Pass template to render.
    # 3.- Pass the context with the data we want to manipulate.
    model = PetOwner # 1 Model
    template_name = 'vet/owners/list.html' # 2 Template
    context_object_name = "owners" # 3 Context
    paginate_by = 6  # Pagination parameter, how many records you want to show per page -> 1
    ordering = '-created_at'  # Sorting results

    # Search bar functionality
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            logger.info(f"Term Searched -> {search_query}")
            queryset = queryset.filter(first_name__icontains=search_query)
            if not queryset:
                messages.warning(self.request, 'No Owners Found!.')
        else:
            logger.warning(f"Empty Term Search")
        return queryset

    # Passing context data (we are passing the search form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class OwnersDetail(LoginRequiredMixin ,DetailView):  # When inheriting from LoginRequiredMixin, you must be logged to access this view
    """Renders a specific Pet Owner with their pk"""
    # 1. Modelo
    # 2. Template to create
    # 3. Context to use on the template
    model = PetOwner
    template_name = 'vet/owners/detail.html'
    context_object_name = "owner"


class PetsList(LoginRequiredMixin ,ListView):
    # Rendering template

    model = Pet  # 1 Model
    template_name = "vet/pets/list.html"  # 2 Template
    context_object_name = "pets"  # 3 Context
    paginate_by = 6  # Pagination parameter, how many records you want to show per page -> 1
    ordering = '-created_at' # Sorting results


    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            logger.info(f"Term Searched -> {search_query}")
            queryset = queryset.filter(name__icontains=search_query)
            if not queryset:
                messages.warning(self.request, 'No Pets Found!.')
        else:
            logger.warning(f"Empty Term Search")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context



class PetsDetail(LoginRequiredMixin, DetailView):
    # Rendering template

    model = Pet
    template_name = "vet/pets/detail.html"
    context_object_name = "pet"


class PetdatesList(LoginRequiredMixin, ListView):
    model = PetDate
    template_name = "vet/petdates/list.html"
    context_object_name = "petdates"
    paginate_by = 6
    ordering = '-datetime'


    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            logger.info(f"Term Searched -> {search_query}")
            queryset = queryset.filter(pet__name__icontains=search_query)
            if not queryset:
                messages.warning(self.request, 'No Appointments Found!.')
        else:
            logger.warning(f"Empty Term Search")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context



class PetdatesDetial(LoginRequiredMixin, DetailView):
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
class OwnersCreate(LoginRequiredMixin, CreateView):
    """View used to create PetOwner"""
    permission_required = "vet.add_petowner"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param

    # 1.- Model
    # 2.- Template to render
    # 3.- Form it's going to be created with
    # 4.- The url if the request was successful and will be redirected to this-> reversed url

    model = PetOwner # 1
    template_name = "vet/owners/create.html" # 2
    form_class = OwnerForm # 3
    success_url = reverse_lazy('vet:owners_list') # 4


    def form_valid(self, form_class):
        messages.success(self.request, 'User Created successfully.')
        return super().form_valid(form_class)





class OwnersUpdate(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    """View used to update a PetOwner"""
    # Permission required to access this view
    # app.action_mode
    permission_required = "vet.change_petowner" #app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next" # related to query param

    model = PetOwner
    template_name = "vet/owners/update.html"
    form_class = OwnerForm # If you want to update specific fields, you can create another form  in forms.py with specific fields

    success_url = reverse_lazy('vet:owners_list')  # 4


    def form_valid(self, form_class):
        messages.success(self.request, 'User Info Updated successfully.')
        return super().form_valid(form_class)



class PetsCreate(LoginRequiredMixin, CreateView):
    """View used to create Pet"""
    permission_required = "vet.add_pet"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param

    model = Pet # 1
    template_name = "vet/pets/create.html" # 2
    form_class = PetForm # 3

    success_url = reverse_lazy('vet:pets_list') # 4

    def form_valid(self, form_class):
        messages.success(self.request, 'Pet Created successfully.')
        return super().form_valid(form_class)


class PetsUpdate(LoginRequiredMixin, UpdateView):
    """View used to update a PetOwner"""
    permission_required = "vet.change_pet"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param


    model = Pet
    template_name =  "vet/pets/update.html"
    form_class = PetForm # If you want to update specific fields, you can create another form  in forms.py with specific fields

    success_url = reverse_lazy('vet:pets_list')  # 4

    def form_valid(self, form_class):
        messages.success(self.request, 'Pet Info Updated successfully.')
        return super().form_valid(form_class)


class PetdatesCreate(LoginRequiredMixin, CreateView):
    """View used to create PetOwner"""
    permission_required = "vet.add_petdate"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param
    # 1.- Model
    # 2.- Template to render
    # 3.- Form it's going to be created with
    # 4.- The url if the request was successful and will be redirected to this-> reversed url

    model = PetDate # 1
    template_name = "vet/petdates/create.html" # 2
    form_class = PetdateForm # 3

    success_url = reverse_lazy('vet:petdates_list') # 4

    def form_valid(self, form_class):
        messages.success(self.request, 'Appointment created successfully.')
        return super().form_valid(form_class)



class PetsdatesUpdate(LoginRequiredMixin, UpdateView):
    """View used to update a PetOwner"""
    permission_required = "vet.change_petdate"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param

    model = PetDate
    template_name =  "vet/petdates/update.html"
    form_class = PetdateForm # If you want to update specific fields, you can create another form  in forms.py with specific fields

    success_url = reverse_lazy('vet:petdates_list')  # 4

    def form_valid(self, form_class):
        messages.success(self.request, 'Appointment Info Updated successfully.')
        return super().form_valid(form_class)



class OwnersDelete(LoginRequiredMixin, DeleteView):
    #permission_required = "vet.delete_petowner"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    #raise_exception = False  # True -> Raise exception when you do not have permission
    #login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    #redirect_field_name = "next"  # related to query param

    model = PetOwner

    template_name = "vet/owners/delete.html"

    success_url = reverse_lazy('vet:owners_list')


    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            # Customize the error message
            messages.warning(self.request, 'Cannot delete Owner.!!')
            error_message = f"Cannot delete owner, has at least one pet related. ({e})"
            return render(request, 'vet/owners/delete.html', {'error_message': error_message})



class PetsDelete(LoginRequiredMixin, DeleteView):
    # This only works four users on admin section
    permission_required = "vet.delete_pet"  # app.how is it named on admin in the group section on permission assigned, just the user with this permission can access to this view
    raise_exception = False  # True -> Raise exception when you do not have permission
    login_url = "/accounts/login/"  # redirect url in case you are not logged, this urls redirect you to the log in admin panel
    redirect_field_name = "next"  # related to query param

    model = Pet
    template_name = "vet/pets/delete.html"

    success_url = reverse_lazy('vet:pets_list')



    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            # Customize the error message
            messages.warning(self.request, 'Cannot delete Pet.!!')
            error_message = f"Cannot delete pet, has at least one related Appointment -> ({e})"
            return render(request, 'vet/pets/delete.html', {'error_message': error_message})



                    # Simple Views Functionalities
# Render text
class Test(View):
    # Como función el método(GET,PATCH,POST.DELETE,PUT)
    def get(self, request):
        return HttpResponse("Hello there, from generic class view!!!")


class GetAllDatesPetdates(View):
        def get(self, request):
            dates = PetDate.objects.all().values('id', 'type', 'datetime')  # Replace 'datetime' with the field name
            events = [{'title': date['type'], 'start': date['datetime'].strftime("%Y-%m-%d %H:%M:%S"), 'color': 'green', 'url': f"petdates/{date['id']}/edit"} for date in dates]
            return JsonResponse(events, safe=False)



class GenerateCSVView(View):
    def post(self, request, *args, **kwargs):
        # Fetch all records from your model
        model_dict = literal_eval(request.body.decode('utf-8'))
        model_selected = model_dict.get('model_view')
        # Storing model data and fields for csv
        model_set, header = get_model_and_fields(model_selected)

        queryset = model_set

        # Create a CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_data.csv"'

        # Create a CSV writer and write data to the response
        writer = csv.writer(response)

        # Write header row (field names) using header variable
        writer.writerow(header)

        # Write data rows
        for item in queryset:
            writer.writerow([getattr(item, field) for field in header])

        return response


class GenericModelAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # Customize this queryset as needed based on your model and field
        model_name = self.kwargs['model_name']
        self.model = apps.get_model(app_label='vet', model_name=model_name)
        qs = model_name.objects.all()

        if model_name == 'Pet':
            if self.q:
                qs = qs.filter(owner__icontains=self.q)

        if model_name == 'PetDate':
            if self.q:
                qs = qs.filter(pet__icontains=self.q)

        return qs


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
            context["pet_date_count"] = PetDate.objects.filter(datetime__year='2023').count()
            pet_date_list = PetDate.objects.all()
            context["pet_date_list"] = [ pet_date_list.datetime.strftime('%Y-%m-%d') for pet_date_list in pet_date_list]
        except PetDate.DoesNotExist:
            context["pet_date_count"] = 0
            context["pet_date_list"] = 0

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


# Helpers
def get_model_and_fields(model_selected):
    model_set = None
    header = None
    if model_selected == 'PetOwner':
        model_set = PetOwner.objects.all()
        # Creating Header for PetOwner  Model
        header = [field.name for field in PetOwner._meta.fields]
    elif model_selected == 'Pet':
        model_set = Pet.objects.all()
        # Creating Header for Pet  Model
        header = [field.name for field in Pet._meta.fields]
    elif model_selected == 'PetDate':
        model_set = PetDate.objects.all()
        # Creating Header for Pet  Model
        header = [field.name for field in PetDate._meta.fields]

    return model_set, header