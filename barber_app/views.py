# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login
# from django.contrib import messages
# from django.db import IntegrityError
# from .models import UserProfile, BarberShop, Service, Appointment
# from .forms import CustomUserCreationForm, BarberShopForm, ServiceForm, AppointmentForm

# def home(request):
#     shops = BarberShop.objects.all()[:6]  # Show first 6 shops
#     return render(request, 'home.html', {'shops': shops})

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             UserProfile.objects.create(
#                 user=user,
#                 user_type=form.cleaned_data['user_type'],
#                 phone=form.cleaned_data['phone'],
#                 address=form.cleaned_data['address']
#             )
#             login(request, user)
#             messages.success(request, 'Registration successful!')
#             return redirect('dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

# @login_required
# def dashboard(request):
#     try:
#         profile = request.user.userprofile
#         if profile.user_type == 'shop_owner':
#             try:
#                 shop = BarberShop.objects.get(owner=request.user)
#                 recent_appointments = Appointment.objects.filter(shop=shop).order_by('-created_at')[:5]
#                 return render(request, 'dashboard/shop_owner.html', {
#                     'shop': shop,
#                     'recent_appointments': recent_appointments
#                 })
#             except BarberShop.DoesNotExist:
#                 return render(request, 'dashboard/shop_owner.html', {'shop': None})
#         else:
#             recent_appointments = Appointment.objects.filter(customer=request.user).order_by('-created_at')[:5]
#             return render(request, 'dashboard/customer.html', {
#                 'recent_appointments': recent_appointments
#             })
#     except UserProfile.DoesNotExist:
#         return redirect('home')

# def shop_list(request):
#     shops = BarberShop.objects.all()
#     return render(request, 'shops/list.html', {'shops': shops})

# def shop_detail(request, shop_id):
#     shop = get_object_or_404(BarberShop, id=shop_id)
#     services = shop.services.all()
#     return render(request, 'shops/detail.html', {'shop': shop, 'services': services})

# @login_required
# def book_appointment(request, shop_id, service_id):
#     shop = get_object_or_404(BarberShop, id=shop_id)
#     service = get_object_or_404(Service, id=service_id, shop=shop)
    
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             try:
#                 appointment = form.save(commit=False)
#                 appointment.customer = request.user
#                 appointment.shop = shop
#                 appointment.service = service
#                 appointment.save()
#                 messages.success(request, 'Appointment booked successfully!')
#                 return redirect('my_appointments')
#             except IntegrityError:
#                 messages.error(request, 'This time slot is already booked. Please choose another time.')
#     else:
#         form = AppointmentForm()
    
#     return render(request, 'appointments/book.html', {
#         'form': form, 'shop': shop, 'service': service
#     })

# @login_required
# def my_appointments(request):
#     appointments = Appointment.objects.filter(customer=request.user).order_by('-appointment_date')
#     return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

# @login_required
# def cancel_appointment(request, appointment_id):
#     appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
#     if appointment.status in ['pending', 'confirmed']:
#         appointment.status = 'cancelled'
#         appointment.save()
#         messages.success(request, 'Appointment cancelled successfully!')
#     return redirect('my_appointments')

# @login_required
# def manage_shop(request):
#     try:
#         profile = request.user.userprofile
#         if profile.user_type != 'shop_owner':
#             messages.error(request, 'Access denied.')
#             return redirect('dashboard')
#     except UserProfile.DoesNotExist:
#         return redirect('home')
    
#     try:
#         shop = BarberShop.objects.get(owner=request.user)
#         shop_form = BarberShopForm(instance=shop)
#     except BarberShop.DoesNotExist:
#         shop = None
#         shop_form = BarberShopForm()
    
#     if request.method == 'POST':
#         if 'shop_form' in request.POST:
#             shop_form = BarberShopForm(request.POST, instance=shop)
#             if shop_form.is_valid():
#                 shop = shop_form.save(commit=False)
#                 shop.owner = request.user
#                 shop.save()
#                 messages.success(request, 'Shop information updated!')
#                 return redirect('manage_shop')
        
#         elif 'service_form' in request.POST and shop:
#             service_form = ServiceForm(request.POST)
#             if service_form.is_valid():
#                 service = service_form.save(commit=False)
#                 service.shop = shop
#                 service.save()
#                 messages.success(request, 'Service added!')
#                 return redirect('manage_shop')
    
#     service_form = ServiceForm()
#     services = shop.services.all() if shop else []
    
#     return render(request, 'dashboard/manage_shop.html', {
#         'shop': shop,
#         'shop_form': shop_form,
#         'service_form': service_form,
#         'services': services
#     })

# @login_required
# def shop_appointments(request):
#     try:
#         shop = BarberShop.objects.get(owner=request.user)
#         appointments = Appointment.objects.filter(shop=shop).order_by('-appointment_date')
#         return render(request, 'dashboard/shop_appointments.html', {
#             'appointments': appointments,
#             'shop': shop
#         })
#     except BarberShop.DoesNotExist:
#         messages.error(request, 'You need to create a shop first.')
#         return redirect('manage_shop')

# @login_required
# def update_appointment_status(request, appointment_id):
#     try:
#         shop = BarberShop.objects.get(owner=request.user)
#         appointment = get_object_or_404(Appointment, id=appointment_id, shop=shop)
        
#         if request.method == 'POST':
#             new_status = request.POST.get('status')
#             if new_status in ['confirmed', 'completed', 'cancelled']:
#                 appointment.status = new_status
#                 appointment.save()
#                 messages.success(request, f'Appointment status updated to {new_status}!')
        
#         return redirect('shop_appointments')
#     except BarberShop.DoesNotExist:
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout  # Added logout here
from django.contrib import messages
from django.db import IntegrityError
from .models import UserProfile, BarberShop, Service, Appointment
from .forms import CustomUserCreationForm, BarberShopForm, ServiceForm, AppointmentForm

def home(request):
    shops = BarberShop.objects.all()[:6]  # Show first 6 shops
    return render(request, 'home.html', {'shops': shops})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
        if profile.user_type == 'shop_owner':
            try:
                shop = BarberShop.objects.get(owner=request.user)
                recent_appointments = Appointment.objects.filter(shop=shop).order_by('-created_at')[:5]
                return render(request, 'dashboard/shop_owner.html', {
                    'shop': shop,
                    'recent_appointments': recent_appointments
                })
            except BarberShop.DoesNotExist:
                return render(request, 'dashboard/shop_owner.html', {'shop': None})
        else:
            recent_appointments = Appointment.objects.filter(customer=request.user).order_by('-created_at')[:5]
            return render(request, 'dashboard/customer.html', {
                'recent_appointments': recent_appointments
            })
    except UserProfile.DoesNotExist:
        return redirect('home')

def shop_list(request):
    shops = BarberShop.objects.all()
    return render(request, 'shops/list.html', {'shops': shops})

def shop_detail(request, shop_id):
    shop = get_object_or_404(BarberShop, id=shop_id)
    services = shop.services.all()
    return render(request, 'shops/detail.html', {'shop': shop, 'services': services})

@login_required
def book_appointment(request, shop_id, service_id):
    shop = get_object_or_404(BarberShop, id=shop_id)
    service = get_object_or_404(Service, id=service_id, shop=shop)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.customer = request.user
                appointment.shop = shop
                appointment.service = service
                appointment.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('my_appointments')
            except IntegrityError:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/book.html', {
        'form': form, 'shop': shop, 'service': service
    })

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(customer=request.user).order_by('-appointment_date')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, customer=request.user)
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
    return redirect('my_appointments')

@login_required
def manage_shop(request):
    try:
        profile = request.user.userprofile
        if profile.user_type != 'shop_owner':
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        return redirect('home')
    
    try:
        shop = BarberShop.objects.get(owner=request.user)
        shop_form = BarberShopForm(instance=shop)
    except BarberShop.DoesNotExist:
        shop = None
        shop_form = BarberShopForm()
    
    if request.method == 'POST':
        if 'shop_form' in request.POST:
            shop_form = BarberShopForm(request.POST, instance=shop)
            if shop_form.is_valid():
                shop = shop_form.save(commit=False)
                shop.owner = request.user
                shop.save()
                messages.success(request, 'Shop information updated!')
                return redirect('manage_shop')
        
        elif 'service_form' in request.POST and shop:
            service_form = ServiceForm(request.POST)
            if service_form.is_valid():
                service = service_form.save(commit=False)
                service.shop = shop
                service.save()
                messages.success(request, 'Service added!')
                return redirect('manage_shop')
    
    service_form = ServiceForm()
    services = shop.services.all() if shop else []
    
    return render(request, 'dashboard/manage_shop.html', {
        'shop': shop,
        'shop_form': shop_form,
        'service_form': service_form,
        'services': services
    })

@login_required
def shop_appointments(request):
    try:
        shop = BarberShop.objects.get(owner=request.user)
        appointments = Appointment.objects.filter(shop=shop).order_by('-appointment_date')
        return render(request, 'dashboard/shop_appointments.html', {
            'appointments': appointments,
            'shop': shop
        })
    except BarberShop.DoesNotExist:
        messages.error(request, 'You need to create a shop first.')
        return redirect('manage_shop')

@login_required
def update_appointment_status(request, appointment_id):
    try:
        shop = BarberShop.objects.get(owner=request.user)
        appointment = get_object_or_404(Appointment, id=appointment_id, shop=shop)
        
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in ['confirmed', 'completed', 'cancelled']:
                appointment.status = new_status
                appointment.save()
                messages.success(request, f'Appointment status updated to {new_status}!')
        
        return redirect('shop_appointments')
    except BarberShop.DoesNotExist:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')
