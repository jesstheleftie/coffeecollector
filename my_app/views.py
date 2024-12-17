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



class CoffeeCreate(LoginRequiredMixin, CreateView):
    model = Coffee
    fields = ['name','roast', 'description', 'roast_age_in_months']
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CoffeeUpdate(LoginRequiredMixin, UpdateView):
    model = Coffee
    # Let's disallow the renaming of a coffee by excluding the name field!
    fields = ['roast', 'description', 'roast_age_in_months']

class CoffeeDelete(LoginRequiredMixin, DeleteView):
    model = Coffee
    success_url = '/coffees/'



class Home(LoginView):
    template_name = 'home.html'
    form_class = CustomAuthenticationForm

def about(request):
    return render(request, 'about.html')

def coffee_index(request):
    coffees = Coffee.objects.filter(user=request.user)
    return render(request, 'coffees/index.html', {'coffees':coffees})



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
        # has the coffee_id assigned
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
 