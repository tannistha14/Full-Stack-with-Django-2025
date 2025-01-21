from django.shortcuts import render

# Create your views here.

# Display the homepage
def home(request):
    return render(request, 'mosaic/home.html')

# Display the menu page
def menu(request):
    return render(request, 'mosaic/menu.html')

