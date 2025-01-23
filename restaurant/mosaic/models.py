from django.db import models
from django.utils.timezone import now
from decimal import Decimal

class menuitem(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizer', 'Appetizer'),
        ('MainCourse', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Drink', 'Drink'),
    ]

    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.CharField(max_length=255, blank=True, null=True)  # Store image path as string
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False)
    is_special = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)  # Add description field

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(menuitem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))



# Reservation Model
class Reservation(models.Model):
    PENDING = "Pending"
    APPROVED = "Approved"
    CANCELLED = "Cancelled"  # Added a CANCELLED status
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (CANCELLED, "Cancelled"),
    ]

    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=10, null=False)
    reservation_date = models.DateTimeField(null=False)
    num_guests = models.IntegerField(null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True, null=True)
    table = models.ForeignKey('Table', on_delete=models.SET_NULL, null=True, blank=True)  # Link table to reservation

    def __str__(self):
        return f"Reservation {self.id} - {self.name}"

    def save(self, *args, **kwargs):
        if self.reservation_date < now():
            raise ValueError("Reservation date cannot be in the past.")
        # Ensure the table is available for this time
        if self.table:
            overlapping_reservations = Reservation.objects.filter(
                table=self.table,
                reservation_date=self.reservation_date,
                status=self.APPROVED
            )
            if overlapping_reservations.exists():
                raise ValueError(f"Table {self.table.table_number} is already reserved at this time.")
        super().save(*args, **kwargs)


# Table and TableData Models
class Table(models.Model):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"
    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (OCCUPIED, "Occupied"),
    ]

    table_number = models.IntegerField(unique=True, null=False)
    capacity = models.IntegerField(null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"


class TableData(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation {self.reservation.id} - Table {self.table.table_number}"

class Cart(models.Model):
    menu_item = models.ForeignKey(menuitem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity})"

