from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from . models import *
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from django.utils import timezone

# Create your views here.
def is_admin(user):
    return user.is_superuser

def index(request):
    return render(request,"index.html")

@user_passes_test(is_admin)
def admin_home(request):
    total_events = Event.objects.count()
    total_students = Student.objects.count()
    total_participants = Registration.objects.filter(is_approved=True).count()
    total_attendance = Attendance.objects.filter(present=True).count()
    upcoming_events = Event.objects.filter(time__gte=timezone.now()).order_by('time')

    return render(request, 'admin_home.html', {
        'total_events': total_events,
        'total_students': total_students,
        'total_participants': total_participants,
        'total_attendance': total_attendance,
        'upcoming_events': upcoming_events,
    })

@user_passes_test(is_admin)
def admin_approve_coordinator(request,cod_id):
    coordinator=get_object_or_404(Coordinator,id=cod_id)
    coordinator.is_coordinator=True
    coordinator.save()
    messages.success(request, f"{coordinator.user.username} approved as coordinator.")
    return redirect('admin_home')

@user_passes_test(is_admin)
def add_category(request):
    if request.method =="POST":
        name=request.POST.get('name')
        Category.objects.create(name=name)
        return redirect("category_list")
    return render(request,"add_category.html")

@user_passes_test(is_admin)
def category_list(request):
    category=Category.objects.all()
    return render(request,"category_list.html",{'category':category})

@user_passes_test(is_admin)
def delete_cat(request,cat_id):
    Category.objects.get(id=cat_id).delete()
    return redirect('category_list')


@user_passes_test(is_admin)
def add_event(request):
    categories=Category.objects.all()
    coordinators=Coordinator.objects.all()
    if request.method=="POST":
        name=request.POST.get('name')
        image=request.FILES.get('image')
        cate_id=request.POST.get('category')
        description=request.POST.get('description')
        time=request.POST.get('time')
        venue=request.POST.get('venue')
        capacity=request.POST.get('capacity')
        is_otp_enabled=bool(request.POST.get('is_otp_enabled'))
        is_feedback_enabled=bool(request.POST.get('is_feedback_enabled'))
        registration_deadline=request.POST.get('registration_deadline')
        coordinator_ids =request.POST.get('coordinators')

        category=Category.objects.get(id=cate_id)

        event=Event.objects.create(
            name=name,
            category=category,
            description=description,
            image=image,
            is_feedback_enabled=is_feedback_enabled,
            is_otp_enabled=is_otp_enabled,
            capacity=capacity,
            time=time,
            venue=venue,
            registration_deadline=registration_deadline,

        )

        for cod_id in coordinator_ids:
            event.coordinators.add(Coordinator.objects.get(id=cod_id))
            return redirect('view_events')

    return render(request, 'add_event.html', {'categories': categories, 'coordinators': coordinators})

@user_passes_test(is_admin)
def edit_event(request,event_id):
    categories=Category.objects.all()
    coordinators=Coordinator.objects.all()
    event=get_object_or_404(Event,id=event_id)
    if request.method =="POST":
        event.name=request.POST.get('name',event.name)
        event.description=request.POST.get('description',event.description)
        event.venue=request.POST.get('venue',event.venue)
        event.time=request.POST.get('time',event.time)
        event.capacity=request.POST.get('capacity',event.capacity)
        event.is_feedback_enabled=bool(request.POST.get('is_feedback_enabled',event.is_feedback_enabled))
        event.is_otp_enabled=bool(request.POST.get('is_otp_enabled',event.is_otp_enabled))
        event.registration_deadline=request.POST.get('registration_deadline',event.registration_deadline)
        if 'image' in request.FILES:
            event.image=request.FILES.get('image')
        cate_id=request.POST.get('category')
        event.category=get_object_or_404(Category,id=cate_id)
        cod_id=request.POST.get('coordinator')
        event.coordinator=get_object_or_404(Coordinator,id=cod_id)
        event.save()
        return redirect('view_events')
    return render(request,"edit_event.html",{'event':event,'coordinators':coordinators,'categories':categories})


@user_passes_test(is_admin)
def view_events(request):
    events = Event.objects.all()
    return render(request, 'view_events.html', {'events': events})

@user_passes_test(is_admin)
def delete_event(request, event_id):
    Event.objects.get(id=event_id).delete()
    return redirect('view_events')

@user_passes_test(is_admin)
def view_registrations(request):
    registrations=Registration.objects.select_related('student','event')
    return render(request,'view_registrations.html', {'registrations': registrations})

@user_passes_test(is_admin)
def update_registration_status(request,reg_id,status):
    registration=Registration.objects.get(id=reg_id)
    if status=="Approved":
        registration.status="Approved"
        registration.is_approved=True
        
    elif status=="Cancelled":
        registration.status="Cancelled"
        registration.is_approved=False
    registration.save()
    messages.success(request, f"Registration {status}d.")
    return redirect('view_registrations')


@user_passes_test(is_admin)
def attendance_report(request,event_id):
    event=Event.objects.get(id=event_id)
    attendances=Attendance.objects.filter(registration__event=event)
    return render(request, 'attendance_report.html', {'event': event, 'attendances': attendances})


@user_passes_test(is_admin)
def view_student(request):
    students=Student.objects.all()
    return render(request,"view_student.html",{'students':students})


@user_passes_test(is_admin)
def view_coordinator(request):
    coordinators=Coordinator.objects.all()
    return render(request,"view_coordinator.html",{'coordinators':coordinators})

@user_passes_test(is_admin)
def promote_student(request,student_id):
    student=Student.objects.get(id=student_id)
    student.is_coordinator=True
    student.save()
    Coordinator.objects.create(user=request.user,is_coordinator=True,phone=student.phone)
    return redirect('view_coordinator')

@user_passes_test(is_admin)
def delete_student(request,student_id):
    Student.objects.get(id=student_id).delete()
    return redirect('view_student')

@user_passes_test(is_admin)
def delete_coordinator(request,code_id):
    Coordinator.objects.get(id=code_id).delete()
    return redirect('view_coordinator')


@user_passes_test(is_admin)
def send_notification(request):
    users = User.objects.all()
    if request.method == "POST":
        message = request.POST.get('message')
        for user in users:
            Notification.objects.create(user=user, message=message, message_type='sms')
        messages.success(request, "Notification sent to all users.")
        return redirect('send_notification')
    return render(request, 'send_notification.html', {'users': users})

@user_passes_test(is_admin)
def event_participation_report(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    registrations=Registration.objects.filter(event=event,is_approved=True)
    attendance=Attendance.objects.filter(registration__in=registrations)
    return render(request,'event_report.html', {
        'event': event,
        'registrations': registrations,
        'attendance': attendance
    })



@user_passes_test(is_admin)
def export_event_report_pdf(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, 800, f"Report for Event: {event.name}")
    y = 760
    for reg in registrations:
        p.drawString(100, y, f"{reg.student.user.username} - {reg.status}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{event.name}_report.pdf")


@user_passes_test(is_admin)
def upload_certificate(request,reg_id):
    registration=get_object_or_404(Registration,id=reg_id,is_approved=True)
    if request.method =="POST" and request.FILES.get('certificate'):
        certificate_file = request.FILES['certificate']
        certificate,created=Certificate.objects.get_or_create(registration=registration)
        certificate.file=certificate_file
        certificate.save() 
        messages.success(request, " Certificate uploaded successfully.")
        return redirect('view_registrations')

    return render(request, 'upload_certificate.html', {'registration': registration})