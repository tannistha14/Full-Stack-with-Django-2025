from django import forms
from django.utils.timezone import now
from .models import Reservation, Table, menuitem

class ReservationForm(forms.ModelForm):
    table = forms.ModelChoiceField(
        queryset=Table.objects.all(),
        required=True,
        empty_label="Select a Table",
        label="Table Number"
    )

    class Meta:
        model = Reservation
        fields = ['name', 'phone_number', 'reservation_date', 'num_guests', 'table']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reservation_date'].widget = forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        })
        # Dynamically filter available tables
        self.fields['table'].queryset = Table.objects.filter(status='Available')

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        reservation_date = cleaned_data.get('reservation_date')

        # Validate overlapping reservations
        if table and reservation_date:
            overlapping_reservations = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date,
                status='Approved'
            )
            if overlapping_reservations.exists():
                raise forms.ValidationError(
                    f"Table {table.table_number} is already reserved at this time."
                )
        return cleaned_data
    # restaurant/mosaic/forms.py

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = menuitem
        fields = ['name', 'description', 'price', 'category', 'image']

