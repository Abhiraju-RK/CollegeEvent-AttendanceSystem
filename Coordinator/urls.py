from django.urls import path
from . import views

urlpatterns=[
    path('coordinator_home',views.coordinator_home,name='coordinator_home'),
    path('register_coordinator',views.register_coordinator,name='register_coordinator'),
    path('coordinator/event/<int:event_id>/registrations/', views.view_event_registrations, name='view_event_registrations'),
    path('update_student_registration/<int:reg_id>/<str:status>/', views.update_student_registration, name='update_student_registration'),
    path('mark_attendance/<int:reg_id>/', views.mark_attendance, name='mark_attendance'),
    path('view_feedback/<int:event_id>/', views.view_feedback, name='view_feedback'),
    path('submit_event_report/<int:event_id>/', views.submit_event_report, name='submit_event_report'),
   
    
]