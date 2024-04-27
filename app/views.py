from django.shortcuts import render,get_object_or_404, redirect
from .models import Event,EventRegistration
from .forms import EventRegistrationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
def home(request):
    return render(request, 'index.html')


def event_list(request):
    events = Event.objects.exclude(approval_status='denied').exclude(approval_status='pending')
    return render(request, 'event-list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registered_users = EventRegistration.objects.filter(event=event,status='IN')
    return render(request, 'event_detials.html', {'event': event, 'registered_users': registered_users})

def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, event_id=event_id)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event_id)  # Redirect to success page
    else:
        form = EventRegistrationForm(event_id=event_id)
    return render(request, 'register.html', {'form': form, 'event': event})


def insert_qr_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_code_message = data.get('data')
        registration = EventRegistration.objects.filter(qr_data=qr_code_message).first()
        if registration:
            # If a matching registration is found, update the status field
            registration.status = 'IN'
            registration.save()
            return JsonResponse({'message': 'QR code matched and status updated successfully'})
        else:
            # If no matching registration is found, just print the message
            print("QR Code Message:", qr_code_message)
            return JsonResponse({'message': 'QR code inserted successfully'})
    else:
        # If the request method is not POST, return a JSON response with an error message
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
def qr(request):
    return render(request, 'qr_scanner.html')