from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('register/', views.register, name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
#     # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('shops/', views.shop_list, name='shop_list'),
#     path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
#     path('book/<int:shop_id>/<int:service_id>/', views.book_appointment, name='book_appointment'),
#     path('my-appointments/', views.my_appointments, name='my_appointments'),
#     path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
#     path('manage-shop/', views.manage_shop, name='manage_shop'),
#     path('shop-appointments/', views.shop_appointments, name='shop_appointments'),
#     path('update-appointment/<int:appointment_id>/', views.update_appointment_status, name='update_appointment'),
# ]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Changed this line
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shops/', views.shop_list, name='shop_list'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('book/<int:shop_id>/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('manage-shop/', views.manage_shop, name='manage_shop'),
    path('shop-appointments/', views.shop_appointments, name='shop_appointments'),
    path('update-appointment/<int:appointment_id>/', views.update_appointment_status, name='update_appointment'),
]

