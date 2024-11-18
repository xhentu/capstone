from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('sign-out/', views.sign_out_view, name='sign-out'),
    path('list/', views.student_list, name='list'),
    
    # Role-based dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher-dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('parent-dashboard/', views.parent_dashboard, name='parent-dashboard'),
]
