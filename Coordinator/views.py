from django.shortcuts import render,redirect,get_object_or_404
from Admin_app.models import Student,Category,Certificate,Coordinator,Feedback,Event,EventReport,Registration,Notification,Attendance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def is_coordinator(user):
    try:
        return user.coordinator.is_coordinator
    except Coordinator.DoesNotExist:
        return False


@user_passes_test(is_coordinator)
def coordinator_home(request):
    coordinator=Coordinator.objects.get(user=request.user)
    events=coordinator.coordinated_events.all()
    notifications = Notification.objects.filter(user=request.user, message_type='sms').order_by('-created_at')
    return render(request, 'coordinator_home.html', {
        'coordinator': coordinator,
        'events': events,
        'notifications':notifications
    })


def register_coordinator(request):
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get("confirm_password")
        phone=request.POST.get('phone')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect("register_coordinator")
        
        if confirm_password!=password:
            messages.error(request,"Passworrd doesnt match")
            return redirect("register_coordinator")
        
        if not phone.isdigit() or  len(phone)!=10:
            messages.error(request,"Phone number must be digit and 10 numbers")
            return redirect("register_coordinator")
        
        user=User.objects.create_user(username=username,password=password)
        Coordinator.objects.create(user=user,phone=phone,is_coordinator=False)
        messages.success(request,"Coordinator registration success Waiting for approvel")
        return redirect("login_page")
    return render(request,"register_coordinator.html")


@user_passes_test(is_coordinator)
def view_event_registrations(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    registrations=Registration.objects.filter(event=event)
    return render(request, 'coordinator_view_registrations.html', {
        'event': event,
        'registrations': registrations
    })
    

@user_passes_test(is_coordinator)
def update_student_registration(request,reg_id,status):
    registration=Registration.objects.get(id=reg_id)
    event_id=registration.event.id
    if status=="Approved":
        registration.status="Approved"
        registration.is_approved=True
        
    elif status=="Cancelled":
        registration.status="Cancelled"
        registration.is_approved=False
    registration.save()
    messages.success(request, f"Registration {status}d.")
    return redirect('view_event_registrations',event_id=event_id)


@user_passes_test(is_coordinator)
def mark_attendance(request,reg_id):
    registration=Registration.objects.get(id=reg_id)
    present=request.GET.get('present')=='true'
    attend,created=Attendance.objects.get_or_create(registration=registration)
    attend.present=present
    attend.save()
    messages.success(request, "Attendance updated.")
    return redirect('view_event_registrations', event_id=registration.event.id)


@user_passes_test(is_coordinator)
def view_feedback(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    feedbacks=Feedback.objects.filter(event=event)
    return render(request, 'coordinator_view_feedback.html', {
        'event': event,
        'feedbacks': feedbacks
    })

@user_passes_test(is_coordinator)
def submit_event_report(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    coordinator=Coordinator.objects.get(user=request.user)
    if request.method =="POST":
        content=request.POST.get('content')
        EventReport.objects.create(event=event,content=content,coordinator=coordinator)
        messages.success(request, "Event report submitted.")
        return redirect('coordinator_home')
    return render(request, 'coordinator_submit_report.html', {'event': event})

