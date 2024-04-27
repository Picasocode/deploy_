
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from .models import Event
staff_group, created = Group.objects.get_or_create(name='staff')
event_content_type = ContentType.objects.get_for_model(Event)

edit_event_permission, created = Permission.objects.get_or_create(
    codename='can_edit_event',
    name='Can edit event',
    content_type=event_content_type,
)

staff_group.permissions.add(edit_event_permission)

staff_users = User.objects.filter(groups__name='staff')
for user in staff_users:
    user.groups.add(staff_group)
