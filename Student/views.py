from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Admin_app.models import Student,Category,Certificate,Coordinator,Feedback,Event,EventReport,Registration,Notification,Attendance
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Q

# Create your views here.
@login_required
def student_home(request):
    student=Student.objects.get(user=request.user)
    certificates=Certificate.objects.filter(registration__student=student)
    register_events=Registration.objects.filter(student=student)
    notifications=Notification.objects.filter(user=request.user,message_type='sms').order_by('-created_at')
    return render(request, 'student_home.html', {
        'student': student,
        'register_events': register_events,
        'certificates': certificates,
        'notifications':notifications
    })

def register_student(request):
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get("confirm_password")
        phone=request.POST.get('phone')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect("register_student")
        
        if confirm_password!=password:
            messages.error(request,"Passworrd doesnt match")
            return redirect("register_student")
        
        if not phone.isdigit() or  len(phone)!=10:
            messages.error(request,"Phone number must be digit and 10 numbers")
            return redirect("register_student")
        
        user=User.objects.create_user(username=username,password=password)
        Student.objects.create(user=user,phone=phone)
        messages.success(request,"Student registration Success")
        return redirect("login_page")
    return render(request,"register_student.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_home')

            coordinator = Coordinator.objects.filter(user=user).first()
            if coordinator:
                if coordinator.is_coordinator:
                    return redirect("coordinator_home")
                else:
                    messages.error(request, "You are not approved as a coordinator yet.")
                    return redirect("login_page")

            student = Student.objects.filter(user=user).first()
            if student:
                return redirect("student_home")

            messages.error(request, "No role assigned to this user.")
            return redirect("login_page")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login_page.html")

def logout_page(request):
    logout(request)
    return redirect("index")


@login_required
def student_events(request):
    events = Event.objects.filter(time__gt=timezone.now()).order_by('time')
    return render(request, 'student_events.html', {
        'events': events,
    })

@login_required
def student_view_event(request,event_id):
    student=Student.objects.get(user=request.user)
    event=get_object_or_404(Event,id=event_id)
    is_registered  =Registration.objects.filter(student=student,event=event).exists()
    feedback=Feedback.objects.filter(event=event)
    return render(request,"student_view_event.html",{'event':event,'feedback':feedback,'is_registered':is_registered})

@login_required
def register_event(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    student=Student.objects.get(user=request.user)

    if timezone.now()>event.registration_deadline:
        messages.error(request, "Registration deadline has passed.")
        return redirect('view_events')
    approved_count=Registration.objects.filter(is_approved=True,event=event).count()
    
    if approved_count>=event.capacity:
        messages.error(request, "Event capacity reached.")
        return redirect('view_events')
    if Registration.objects.filter(event=event, student=student).exists():
        messages.warning(request, "You have already registered for this event.")
        return redirect('view_events')

    Registration.objects.create(event=event, student=student)
    messages.success(request, "Registration submitted. Waiting for approval.")
    return redirect('student_home')


@login_required
def view_attendance(request):
    student=get_object_or_404(Student,user=request.user)
    attendance=Attendance.objects.filter(registration__student=student)
    return render(request, 'student_view_attendance.html', {'attendance': attendance})

@login_required
def submit_feedback(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    student=Student.objects.get(user=request.user)

    if request.method =="POST":
        text=request.POST.get('text')
        Feedback.objects.create(text=text,event=event,student=student)
        messages.success(request, "Feedback submitted.")
        return redirect('student_view_event',event_id=event.id)
    
    return render(request, 'submit_feedback.html', {'event': event})


@login_required
def view_certificates(request):
    student=Student.objects.get(user=request.user)
    certificates=Certificate.objects.filter(registration__student=student)
    return render(request, 'view_certificates.html', {'certificates': certificates})


@login_required
def search_event(request):
    search_query=request.GET.get('q','')
    events=Event.objects.all()
    if search_query:
        search_query=events.filter(Q(category__name__icontains=search_query)|Q(name__icontains=search_query))
    return render(request,"search_event.html",{'events':events,'search_query':search_query})