from django.urls import path
from . import views

urlpatterns=[
    path('student_home',views.student_home,name='student_home'),
    path('register_student',views.register_student,name='register_student'),
    path('login_page',views.login_page,name='login_page'),
    path('logout_page',views.logout_page,name='logout_page'),
    path('student_events', views.student_events, name='student_events'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),
    path('view_attendance', views.view_attendance, name='view_attendance'),
    path('submit_feedback/<int:event_id>/', views.submit_feedback, name='submit_feedback'),
    path('view_certificates', views.view_certificates, name='view_certificates'),
    path('student_view_event/<int:event_id>/',views.student_view_event,name='student_view_event'),
    path('search_event',views.search_event,name='search_event'),

    
]