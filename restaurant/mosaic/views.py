from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import menuitem, Order, Reservation, Table, OrderItem, Cart
from .forms import ReservationForm, MenuItemForm

def home(request):
    return render(request, 'mosaic/home.html')

def menu(request):
    categories = ['Appetizer', 'MainCourse', 'Dessert', 'Drink']
    context = {category.lower(): menuitem.objects.filter(category=category) for category in categories}
    return render(request, 'mosaic/menu.html', context)

def dashboard(request, section=None):
    total_reservations = Reservation.objects.count()
    total_income = OrderItem.objects.aggregate(total=Sum('total_price'))['total'] or 0
    tables = Table.objects.all()
    
    if section == "menu":
        items = menuitem.objects.all()
        return render(request, 'mosaic/manage_menu.html', {'items': items})
    elif section == "order":
        orders = Order.objects.all()
        return render(request, 'mosaic/manage_order.html', {'orders': orders})
    elif section == "reservation":
        reservations = Reservation.objects.select_related('table').all()
        return render(request, 'mosaic/manage_reservation.html', {'reservations': reservations})
    
    return render(request, 'mosaic/dashboard.html', {
        'total_orders': OrderItem.objects.count(),
        'total_reservations': total_reservations,
        'total_income': total_income,
        'tables': tables,
    })

def menu_view(request, category):
    categories = {
        'appetizers': 'Appetizer',
        'main_course': 'MainCourse',
        'desserts': 'Dessert',
        'drinks': 'Drink'
    }
    category_name = categories.get(category.lower())
    items = menuitem.objects.filter(category=category_name) if category_name else []
    return render(request, 'mosaic/menu_category.html', {'category': category.title(), 'items': items})

def edit_menu_item(request, id):
    instance = get_object_or_404(menuitem, id=id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('dashboard', section='menu')
    else:
        form = MenuItemForm(instance=instance)
    return render(request, 'mosaic/dashboard/edit_menu_item.html', {'form': form})

def delete_menu_item(request, id):
    instance = get_object_or_404(menuitem, id=id)
    if request.method == 'POST':
        instance.delete()
        return redirect('dashboard', section='menu')
    return render(request, 'mosaic/dashboard/confirm_delete.html', {'item': instance})

def approve_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'Approved'
    reservation.save()
    return redirect('dashboard', section='reservation')

def reject_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    reservation.status = 'Rejected'
    reservation.save()
    return redirect('dashboard', section='reservation')

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            reservation.table.status = 'Reserved'
            reservation.table.save()
            messages.success(request, f"Reservation created for Table {reservation.table.table_number}!")
            return redirect('reservation')
    else:
        form = ReservationForm()
    reservations = Reservation.objects.order_by('-reservation_date')
    return render(request, 'mosaic/reservation.html', {'form': form, 'reservations': reservations})

def add_to_cart(request, item_id):
    menu_item = get_object_or_404(menuitem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = Cart.objects.get_or_create(menu_item=menu_item)
    cart_item.quantity = cart_item.quantity + quantity if not created else quantity
    cart_item.save()
    messages.success(request, f"{menu_item.name} added to cart!")
    return redirect('order')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('order')

def order(request):
    cart_items = Cart.objects.all()
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    return render(request, 'mosaic/order.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    cart_items = Cart.objects.all()
    if request.method == 'POST':
        total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
        order = Order.objects.create(total_price=total_price, status="Pending")
        for item in cart_items:
            OrderItem.objects.create(order=order, menu_item=item.menu_item, quantity=item.quantity, price=item.menu_item.price, total_price=item.menu_item.price * item.quantity)
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation')
    return redirect('order')

def order_confirmation(request):
    return render(request, 'mosaic/order_confirmation.html')
