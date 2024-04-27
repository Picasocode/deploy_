from django.contrib import admin
from .models import Event,EventRegistration
from import_export.admin import ImportExportModelAdmin
from .resources import ReportResource, UserResource
from .forms import UserSelectForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
from django import forms
import base64
import pandas as pd
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os

def send_email(to_email, reg, name, year,attachment_path):
    subject = "Congratulations!"
    from_email = 'cybertrixofficials@gmail.com'
    recipient_list = [to_email]

    html_content = html_content = f"""
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Design</title>
</head>
<body style="font-family: 'Roboto Mono', monospace; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0;">

<div class="card" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 30px; transition: transform 0.3s ease; width: 300px;">
    <h2 style="color: #333; margin-bottom: 15px; font-size: 1.5rem;">Congratulations!</h2>
    <p style="margin-bottom: 10px; font-size: 1rem; color: #000;">Mr/Ms {name},</p>
    <p style="margin-bottom: 10px; font-size: 1rem; color: #000;text-align: justify;">Congratulations on getting shortlisted and selected to be part of the Cybertrix Club. Looking forward to working with you in future events and club activities!</p>
    <hr style="border: none; border-top: 1px solid #ddd; margin-bottom: 15px;">
    <p><b style="font-size: 1rem;">Name:</b> {name}</p>
    <p><b style="font-size: 1rem;">Register Number:</b> {reg}</p>
    <p><b style="font-size: 1rem;">Year:</b> {year} year</p>
    <div style="display: flex; justify-content: center;">
        <img src="http://cybertrix.byethost12.com/logo-1.png" alt="Club Logo">
    </div>
</div>


</body>
</html>
    """
    email = EmailMessage(subject, html_content, from_email, recipient_list)
    email.content_subtype = "html"
    attachment_file = open(attachment_path, 'rb')
    email.attach(os.path.basename(attachment_path), attachment_file.read(), 'image/png')  # Adjust mimetype as needed
    attachment_file.close()
    email.send()


    print(f'Email to {to_email} with body and logo sent successfully!')




class EventModelAdmin(ImportExportModelAdmin):
    resource_class = ReportResource

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'user' in form.base_fields:  # Check if 'user' field is present in the form
            form.base_fields['user'].initial = request.user
        return form


    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
        # Restrict access to 'approval_status' for non-superusers
            readonly_fields += ('approval_status',)
        # Show 'denial_reason' for denied events
            if obj and obj.approval_status == 'denied':
                readonly_fields += ('denial_reason',)
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.approval_status != 'denied' and not request.user.is_superuser:
            fieldsets[0][1]['fields'] = [field for field in fieldsets[0][1]['fields'] if field != 'denial_reason']
        return fieldsets

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset

    list_display = ('Event_Name', 'Event_Start_Date', 'Event_End_Date', 'Event_Start_Time', 'Event_End_Time','Broucher_','approval_status')
    def Broucher_(self, obj):
        return format_html('<img src="{}" width="100" height="auto" />', obj.Broucher.url)

    Broucher_.short_description = 'Broucher'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if the event is being added
            obj.user = request.user  # Assign the current user as the event creator
        super().save_model(request, obj, form, change)


    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superusers can edit events unconditionally
        if obj is not None:
            current_datetime = timezone.now()
            if obj.Event_Start_Date <= current_datetime.date() <= obj.Event_End_Date:
                current_time = current_datetime.time()
                start_time_choices = dict(obj._meta.get_field('Event_Start_Time').choices)
                end_time_choices = dict(obj._meta.get_field('Event_End_Time').choices)
                start_time = start_time_choices.get(current_time.replace(second=0, microsecond=0))  # Get the display value for the current time
                end_time = end_time_choices.get(current_time.replace(second=0, microsecond=0))  # Get the display value for the current time
                if start_time and end_time:
                    return True
        return False

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if the event is being added
            obj.user = request.user  # Assign the current user as the event creator
        super().save_model(request, obj, form, change)

class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    resource_class = UserResource

class EventRegAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Register_No', 'year', 'Department', 'Section', 'Event_Name', 'Email','qr_code_image' )
    resource_class = ReportResource
    search_fields = ('Name', 'Register_No', 'year', 'Department', 'Event_Name', 'Email')
    list_filter = ('year', 'Department', 'Event_Name', 'registration_date')
    ordering = ('-registration_date',)
    def qr_code_image(self, obj):
        if obj.QR_Code:
            return format_html('<img src="{}" width="50" height="50" />', obj.QR_Code.url)
        else:
            return '-'

    qr_code_image.short_description = 'QR Code'
    actions = ['custom_action']
    def custom_action(self, request, queryset):
        for registration in queryset:
            to_email = registration.Email
            reg = registration.Register_No
            name = registration.Name
            year = registration.year
            attachment_path = registration.QR_Code.url
            print(attachment_path)
            try:
                send_email(to_email, reg, name, year,attachment_path)
                self.message_user(request, f"Email sent successfully to {to_email}.")
            except Exception as e:
                self.message_user(request, f"Error sending email to {to_email}: {str(e)}", level='error')
            
        return None
        self.message_user(request, "Custom action executed successfully.")
        
    custom_action.short_description = "Send Mail"


admin.site.register(Event, EventModelAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(EventRegistration,EventRegAdmin)
