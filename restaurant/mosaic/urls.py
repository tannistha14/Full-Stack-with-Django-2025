from django.urls import path
from .views import home, menu

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('menu', menu, name='menu'),  # Menu page URL
]
