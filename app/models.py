import qrcode
import datetime
from io import BytesIO
from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
class Event(models.Model):
    APPROVAL_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Event_Name = models.CharField(max_length=100)
    Event_Title = models.TextField()
    Event_Venue = models.CharField(max_length=1000,default="SCAS")
    Event_Start_Date = models.DateField()
    Event_End_Date = models.DateField()
    START_TIME_CHOICES = [(datetime.time(hour=h, minute=0), f'{h % 12 or 12}:00 {("AM" if h < 12 else "PM")}') for h in range(24)]
    END_TIME_CHOICES = START_TIME_CHOICES
    Event_Start_Time = models.TimeField(choices=START_TIME_CHOICES)
    Event_End_Time = models.TimeField(choices=END_TIME_CHOICES)
    Broucher = models.ImageField(upload_to = "broucher")
    Chief_Patrons = models.TextField(default="Dr. MARIAZEENA JOHNSON, CHANCELLOR| Dr. MARIE JOHNSON, PRESIDENT| Ms. MARIA CATHERINE JAYAPRIYA,VICE PRESIDENT")
    Patrons = models.TextField(default="Dr. T. SASIPRABA, VICE CHANCELLOR")
    Convenors=models.TextField(default="Format:Name1,Name 2")
    Facult_Coordinator=models.TextField(default="Format:Name1,Name 2")
    Student_Coordinator=models.TextField(default="Format:Name1,Name 2")
    approval_status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='pending')
    denial_reason = models.TextField(blank=True)

    def __str__(self):
        return self.Event_Name

    class Meta:
        permissions = [
            ("can_edit_event", "Can edit event"),
        ]


class EventRegistration(models.Model):
    APPROVAL_CHOICES = (
        ('NOT IN', 'NOT IN'),
        ('IN', 'IN'),
    )
    SECTION_CHOICES = (
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A3', 'A3'),
        ('A4', 'A4'),
        ('A5', 'A5'),
        ('B1', 'B1'),
        ('B2', 'B2'),
    )
    SPECIALIZATION_CHOICES = (
        ('B.E CSE - Artificial Intelligence', 'B.E CSE - Artificial Intelligence'),
        ('B.E CSE - Data Science', 'B.E CSE - Data Science'),
        ('B.E CSE - Internet of Things', 'B.E CSE - Internet of Things'),
        ('B.E CSE - Artificial Intelligence and Robotics', 'B.E CSE - Artificial Intelligence and Robotics'),
        ('B.E CSE - Artificial Intelligence and Machine Learning', 'B.E CSE - Artificial Intelligence and Machine Learning'),
        ('B.E CSE - Block Chain Technology', 'B.E CSE - Block Chain Technology'),
        ('B.E CSE - Cyber Security', 'B.E CSE - Cyber Security'),
        ('Others','Others'),
    )
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1000)
    Register_No=models.CharField(max_length=1000)
    year = models.CharField(max_length=1000,choices=YEAR_CHOICES)
    Department=models.CharField(max_length=1000)
    Specialization=models.CharField(max_length=1000, choices=SPECIALIZATION_CHOICES )
    Section=models.CharField(max_length=1000,choices=SECTION_CHOICES)
    Event_Name = models.CharField(max_length=1000)
    Email = models.EmailField()
    Phone_No = models.CharField(max_length=1000)
    registration_date = models.DateTimeField(auto_now_add=True)
    QR_Code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_data = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=APPROVAL_CHOICES, default='NOT_IN')
    def __str__(self):
        return f"{self.Name} - {self.Event_Name}"
    
    class Meta:
        unique_together = [['Register_No', 'Event_Name']]

@receiver(post_save, sender=EventRegistration)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:  # Only generate QR code for new registrations
        qr_data = f"Name: {instance.Name}\n" \
                  f"Register No: {instance.Register_No}\n" \
                  f"Year: {instance.year}\n" \
                  f"Department: {instance.Department}\n" \
                  f"Section: {instance.Section}\n" \
                  f"Event Name: {instance.Event_Name}\n" \
                  f"Email: {instance.Email}\n" \
                  f"Registration Date: {instance.registration_date}"
        
        instance.qr_data = qr_data  # Save QR data to the model
        
        qr = qrcode.make(qr_data)
        temp_buffer = BytesIO()
        qr.save(temp_buffer, format='PNG')
        temp_buffer.seek(0)

        instance.QR_Code.save(f"qr_{instance.Register_No}_{instance.Event_Name}.png", File(temp_buffer), save=True)
