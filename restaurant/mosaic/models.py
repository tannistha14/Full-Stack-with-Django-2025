from django.db import models
from django.utils.timezone import now

# Centralized MenuItem Model
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Appetizer', 'Appetizer'),
        ('MainCourse', 'Main Course'),
        ('Dessert', 'Dessert'),
        ('Drink', 'Drink'),
    ]

    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=False)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    PENDING = "Pending"
    COMPLETE = "Complete"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
    ]

    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    customer_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

# Reservation Model
class Reservation(models.Model):
    PENDING = "Pending"
    APPROVED = "Approved"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
    ]

    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=10, null=False)
    reservation_date = models.DateTimeField(null=False)
    num_guests = models.IntegerField(null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True, null=True)  # Special instructions

    def __str__(self):
        return f"Reservation {self.id} - {self.name}"

    def save(self, *args, **kwargs):
        if self.reservation_date < now():
            raise ValueError("Reservation date cannot be in the past.")
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