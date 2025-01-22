from django import forms
from .models import MenuItem, Reservation

# Form for creating/editing MenuItems
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image', 'category', 'is_special']
        
    # Optional: You can add custom validations or clean methods for fields if needed

# Form for creating/editing Reservations
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'reservation_date', 'num_guests', 'notes']
        
    # Optional: You can add custom validations for reservation-specific fields if needed

