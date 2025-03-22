from django.urls import path

from django.contrib import admin
from .views import (
    triple_forms_view,
    login_view,
    register_view,
    forgot_password_view,
    dashboard_view,
    logout_view,
    chat_view,
    barcode_scanner_view,
    extra_data_view,
    update_settings,
    log_meal_view,
    update_profile,
    chat_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('triple/', triple_forms_view, name='triple_forms'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('forgot_password/', forgot_password_view, name='forgot_password'),
    path('extra-data/', extra_data_view, name='extra_data'),
    path('log_meal/', log_meal_view, name='log_meal'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('chat/', chat_view, name='chat'),
    path('barcode/', barcode_scanner_view, name='barcode_scanner'),
    path('update_settings/', update_settings, name='update_settings'),
    path("update_profile/", update_profile, name="update_profile"),
    path("chat/", chat_view, name="chat"),
]
