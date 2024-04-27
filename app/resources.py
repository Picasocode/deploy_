from import_export import resources 
from .models import Event,EventRegistration
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export import resources, fields
class ReportResource(resources.ModelResource):
    user_username = fields.Field(attribute='user__username', column_name='User Username')

    class Meta:
         model = Event

class UserResource(resources.ModelResource):
    
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email')

class EventResource(resources.ModelResource):
    
    class Meta:
        model = EventRegistration
        fields = ('Name', 'Register_No', 'year', 'Department', 'Section', 'Class_No', 'Event_Name',)
