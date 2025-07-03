from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, BarberShop, Service, Appointment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__email']

@admin.register(BarberShop)
class BarberShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'owner__username']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'duration_minutes']
    list_filter = ['shop']
    search_fields = ['name', 'shop__name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'shop', 'service', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date', 'shop']
    search_fields = ['customer__username', 'shop__name']
    date_hierarchy = 'appointment_date'
