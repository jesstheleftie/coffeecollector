from django.urls import path, include
from . import views # Import views to connect routes to view functions
from django.contrib import admin
urlpatterns = [
    # Routes will be added here
  
    path('about/', views.about, name='about'),
    path('coffees/', views.coffee_index, name='coffee-index'),
    path('coffees/<int:coffee_id>', views.coffee_detail, name='coffee-detail'),
    path('coffees/create/', views.CoffeeCreate.as_view(), name='coffee-create'),
    path('coffees/<int:pk>/update/', views.CoffeeUpdate.as_view(), name='coffee-update'),
    path('coffees/<int:pk>/delete/', views.CoffeeDelete.as_view(), name='coffee-delete'),
    path('coffees/<int:coffee_id>/add-rating/', views.add_rating, name='add-rating'),
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),

]

