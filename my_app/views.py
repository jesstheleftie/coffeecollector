from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Coffee
from .forms import RatingForm
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
# Add the two imports below
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomAuthenticationForm

# class Coffee:
#     def __init__(self, name, roast, description, roast_age_in_months):
#         self.name = name
#         self.roast = roast
#         self.description = description
#         self.roast_age_in_months = roast_age_in_months

# coffees = [
#     Coffee('Tropical Punch', 'light', 'Fruity and sweet.', 6),
#     Coffee('Holiday Espresso', 'medium', 'Gingerbread spice and chocolaty', 2),
#     Coffee('Old School', 'dark', 'Caramel and nutty', 3),
#     Coffee('Grinch', 'dark', 'Molasses and liquorice', 5)
# ]
# Create your views here.
# main-app/views.py

class CoffeeCreate(LoginRequiredMixin, CreateView):
    model = Coffee
    fields = ['name','roast', 'description', 'roast_age_in_months']
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CoffeeUpdate(LoginRequiredMixin, UpdateView):
    model = Coffee
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['roast', 'description', 'roast_age_in_months']

class CoffeeDelete(LoginRequiredMixin, DeleteView):
    model = Coffee
    success_url = '/coffees/'


# Import HttpResponse to send text-based responses
# from django.http import HttpResponse

# Define the home view function
# def home(request):
#     # Send a simple HTML response
#     return render(request, 'home.html')
class Home(LoginView):
    template_name = 'home.html'
    form_class = CustomAuthenticationForm

def about(request):
    return render(request, 'about.html')

def coffee_index(request):
    coffees = Coffee.objects.filter(user=request.user)
    return render(request, 'coffees/index.html', {'coffees':coffees})


# def coffee_detail(request, coffee_id):
#     coffee = Coffee.objects.get(id=coffee_id)
#     return render(request, 'coffees/detail.html', {'coffee': coffee})
@login_required 
def coffee_detail(request, coffee_id):
    coffee = Coffee.objects.get(id=coffee_id)
    
    rating_form = RatingForm()
    return render(request, 'coffees/detail.html', {
        
        'coffee': coffee, 'rating_form': rating_form
    })
@login_required 
def add_rating(request, coffee_id):
    # create a ModelForm instance using the data in request.POST
    form = RatingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_rating = form.save(commit=False)
        new_rating.coffee_id = coffee_id
        new_rating.save()
    return redirect('coffee-detail', coffee_id=coffee_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('coffee-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
 