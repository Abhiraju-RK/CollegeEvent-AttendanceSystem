from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=12)
    is_coordinator=models.BooleanField(blank=True,null=True,default=False)

    def __str__(self):
        return self.user.username
    
class Coordinator(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=12)
    is_coordinator=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.FileField(upload_to='images/')
    description = models.TextField()
    venue = models.CharField(max_length=100)
    time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    is_feedback_enabled = models.BooleanField(default=False)
    is_otp_enabled = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_events')
    coordinators = models.ManyToManyField(Coordinator, related_name='coordinated_events')


class Registration(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(max_length=30,choices=[('Pending','Pending'),('Approved','Approved'),('Cancelled','Cancelled')],default='Pending')
    is_approved=models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    verified_by_otp = models.BooleanField(default=False)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    message_type = models.CharField(max_length=20, choices=[('email', 'Email'), ('sms', 'SMS'), ('push', 'Push')])
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class EventReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    coordinator = models.ForeignKey(Coordinator, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    file = models.FileField(upload_to='certificates/')
