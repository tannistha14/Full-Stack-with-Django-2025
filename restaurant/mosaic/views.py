from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import MenuItem, Order, Reservation, Table, OrderItem
from .forms import ReservationForm

def home(request):
    """Render the home page."""
    return render(request, 'mosaic/home.html')

def menu(request):
    """Render the menu page with all categories."""
    appetizers = MenuItem.objects.filter(category='Appetizer')
    main_courses = MenuItem.objects.filter(category='MainCourse')
    desserts = MenuItem.objects.filter(category='Dessert')
    drinks = MenuItem.objects.filter(category='Drink')
    
    context = {
        'appetizers': appetizers,
        'main_courses': main_courses,
        'desserts': desserts,
        'drinks': drinks,
    }
    return render(request, 'mosaic/menu.html', context)

def order(request):
    """Render the order page."""
    orders = Order.objects.all()
    return render(request, 'mosaic/order.html', {'orders': orders})

def dashboard(request, section=None):
    """Render the admin dashboard with summary data."""
    total_orders = Order.objects.count()
    total_reservations = Reservation.objects.count()
    total_income = OrderItem.objects.aggregate(total=Sum('menu_item__price'))['total'] or 0
    tables = Table.objects.all()

    if section == "menu":
        items = MenuItem.objects.all()
        return render(request, 'mosaic/manage_menu.html', {'items': items})

    elif section == "order":
        orders = Order.objects.all()
        return render(request, 'mosaic/manage_order.html', {'orders': orders})

    elif section == "reservation":
        reservations = Reservation.objects.select_related('table').all()
        return render(request, 'mosaic/manage_reservation.html', {'reservations': reservations})

    context = {
        'total_orders': total_orders,
        'total_reservations': total_reservations,
        'total_income': total_income,
        'tables': tables,
    }
    return render(request, 'mosaic/dashboard.html', context)


def menu_view(request, category):
    """Dynamic view for menu categories."""
    category_display_names = {
        'appetizers': 'Appetizer',
        'main_course': 'MainCourse',
        'desserts': 'Dessert',
        'drinks': 'Drink'
    }

    # Get the correct category name or return an empty list if the category is invalid
    category_name = category_display_names.get(category.lower())
    items = MenuItem.objects.filter(category=category_name) if category_name else []

    return render(request, 'mosaic/menu_category.html', {
        'category': category.replace('_', ' ').title(),
        'items': items
    })


def edit_menu_item(request, model, id):
    """Generic edit view for menu items."""
    model_map = {
        'appetizer': (MenuItem, MenuItemForm),
        'main_course': (MenuItem, MenuItemForm),
        'dessert': (MenuItem, MenuItemForm),
        'drink': (MenuItem, MenuItemForm)
    }
    model_class, form_class = model_map.get(model)
    instance = get_object_or_404(model_class, id=id)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = form_class(instance=instance)

    return render(request, f'mosaic/dashboard/edit_{model}.html', {'form': form})

def delete_menu_item(request, model, id):
    """Generic delete view for menu items."""
    model_map = {
        'appetizer': MenuItem,
        'main_course': MenuItem,
        'dessert': MenuItem,
        'drink': MenuItem
    }
    model_class = model_map.get(model)
    instance = get_object_or_404(model_class, id=id)

    if request.method == 'POST':
        instance.delete()
        return redirect('dashboard')

    return render(request, 'mosaic/dashboard/confirm_delete.html', {'item': instance})

# New view to approve a reservation
def approve_reservation(request, id):
    """Approve a reservation."""
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'Approved'
    reservation.save()
    return redirect('reservation')

# New view to reject a reservation
def reject_reservation(request, id):
    """Reject a reservation."""
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'Rejected'
    reservation.save()
    return redirect('reservation')

def reservation(request):
    """Handle new reservations."""
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            table = form.cleaned_data.get('table')
            # Update table status to reserved
            if table:
                table.status = 'Reserved'
                table.save()
            reservation.save()
            messages.success(request, f"Reservation created for Table {table.table_number}!")
            return redirect('reservation')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReservationForm()

    reservations = Reservation.objects.order_by('-reservation_date')
    return render(request, 'mosaic/reservation.html', {'form': form, 'reservations': reservations})


    # Other sections of the dashboard

