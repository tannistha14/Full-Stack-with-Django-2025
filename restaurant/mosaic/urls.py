from django.urls import path
from .views import home, menu, order, reservation, dashboard, menu_view, approve_reservation, reject_reservation

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('menu/', menu, name='menu'),  # Added trailing slash for consistency
    path('order/', order, name='order'),
    path('reservation/', reservation, name='reservation'),
    path('dashboard/', dashboard, name='dashboard'),  # Admin dashboard URL
    path('dashboard/<str:section>/', dashboard, name='manage_dashboard'),  # For manage sections like menu, order, reservation
    path('menu/<str:category>/', menu_view, name='menu_category'),
    path('reservation/approve/<int:id>/', approve_reservation, name='approve_reservation'),
    path('reservation/reject/<int:id>/', reject_reservation, name='reject_reservation'),
    
]
