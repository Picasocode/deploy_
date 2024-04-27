from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from admin_notification.views import check_notification_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('check/notification', check_notification_view, name="check_notifications"),
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('qr_code/', views.qr, name='qr'),      
    path('insert_qr_code/', views.insert_qr_code, name='insert_qr_code'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
