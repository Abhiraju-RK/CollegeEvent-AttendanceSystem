from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_cat/<int:cat_id>/',views.delete_cat,name='delete_cat'),
    path('category_list',views.category_list,name='category_list'),
    path('add_event', views.add_event, name='add_event'),
    path('view_events',views.view_events,name='view_events'),
    path('delete_event/<int:event_id>/',views.delete_event,name='delete_event'),
    path('delete_coordinator/<int:code_id>/',views.delete_coordinator,name='delete_coordinator'),
    path('delete_student/<int:student_id>/',views.delete_student,name='delete_student'),
    path('view_student',views.view_student,name='view_student'),
    path('view_coordinator',views.view_coordinator,name='view_coordinator'),
    path('view_registrations/', views.view_registrations, name='view_registrations'),
    path('attendance_report/<int:event_id>/',views.attendance_report,name='attendance_report'),
    path('update_registration_status/<int:reg_id>/<str:status>/', views.update_registration_status, name='update_registration_status'),
    path('promote_student/<int:student_id>/', views.promote_student, name='promote_student'),
    path('send_notification', views.send_notification, name='send_notification'),
    path('event_participation_report/<int:event_id>/', views.event_participation_report, name='event_participation_report'),
    path('export_event_report_pdf/<int:event_id>/', views.export_event_report_pdf, name='export_event_report_pdf'),
    path('admin_approve_coordinator/<int:cod_id>/',views.admin_approve_coordinator,name='admin_approve_coordinator'),
    path('upload_certificate/<int:reg_id>/', views.upload_certificate, name='upload_certificate'),
    path('edit_event/<int:event_id>/',views.edit_event,name='edit_event'),


]