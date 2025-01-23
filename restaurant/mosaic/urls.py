from django.urls import path
from .views import home, menu, order, reservation, dashboard, menu_view, approve_reservation, reject_reservation, add_to_cart, checkout, remove_from_cart, order_confirmation

urlpatterns = [
    path('', home, name='home'),  # Home page URL
    path('menu/', menu, name='menu'),  # Menu page URL
    path('order/', order, name='order'),  # Order page URL
    path('reservation/', reservation, name='reservation'),  # Reservation page URL
    path('dashboard/', dashboard, name='dashboard'),  # Admin dashboard URL
    path('dashboard/<str:section>/', dashboard, name='manage_dashboard'),  # For manage sections like menu, order, reservation
    path('menu/<str:category>/', menu_view, name='menu_category'),  # Menu category URL
    path('reservation/approve/<int:id>/', approve_reservation, name='approve_reservation'),  # Approve reservation URL
    path('reservation/reject/<int:id>/', reject_reservation, name='reject_reservation'),  # Reject reservation URL
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),  # Add item to cart URL
    path('checkout/', checkout, name="checkout"),  # Checkout URL
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),  # Remove item from cart URL
    path('order_confirmation/', order_confirmation, name='order_confirmation'),  # Order confirmation URL
]
