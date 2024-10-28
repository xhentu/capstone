# core/views.py
from django.shortcuts import render, get_object_or_404
from users.models import StudentProfile, CustomUser
from core.models import ExamGrade, Fees
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Import models from core
from core.models import (
    AcademicYear, Grade, Class, Subject, Schedule, TeacherAssignment,
    StudentEnrollment, Attendance, Exam, ExamGrade, Fees, Notification,
    TeacherDailyAttendance, StaffDailyAttendance
)

# Import models from users
from users.models import (
    CustomUser, AdminProfile, StaffProfile, TeacherProfile, 
    StudentProfile, ParentProfile, SalaryPayment
)

User = get_user_model()

def student_list(request):
    students = StudentProfile.objects.all()
    print("Number of students:", students.count())  # Add this line
    return render(request, 'core/layout.html', {'students': students})

def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print("Attempting login with:", username, password)  # Debug print

        user = authenticate(request, username=username, password=password)
        if user is None:
            print("Authentication failed for:", username)
            return render(request, 'core/sign_in.html', {'error': 'Invalid username or password.'})

        login(request, user)
        role = user.role

        # Redirect based on role
        if role == 'admin':
            return redirect('admin-dashboard')
        elif role == 'staff':
            return redirect('staff-dashboard')
        elif role == 'teacher':
            return redirect('teacher-dashboard')
        elif role == 'student':
            return redirect('student-dashboard')
        elif role == 'parent':
            return redirect('parent-dashboard')
        else:
            return render(request, 'core/error.html', {'message': 'Unknown role'})

    return render(request, 'core/sign_in.html')

def sign_out_view(request):
    logout(request)
    return redirect('sign-in')  # Redirect to sign-in page after logging out

def admin_dashboard(request):
    academic_years = AcademicYear.objects.all()
    staff_profiles = StaffProfile.objects.all()
    teacher_profiles = TeacherProfile.objects.all()
    student_profiles = StudentProfile.objects.all()
    exams = Exam.objects.all()

    return render(request, 'admin_dashboard.html', {
        'academic_years': academic_years,
        'staff_profiles': staff_profiles,
        'teacher_profiles': teacher_profiles,
        'student_profiles': student_profiles,
        'exams': exams,
    })

def staff_dashboard(request):
    user = request.user
    staff_profile = StaffProfile.objects.get(user=user)
    salary_payments = SalaryPayment.objects.filter(profile=user)

    return render(request, 'staff_dashboard.html', {
        'staff_profile': staff_profile,
        'salary_payments': salary_payments,
    })

def teacher_dashboard(request):
    user = request.user
    teacher_profile = TeacherProfile.objects.get(user=user)
    assigned_classes = TeacherAssignment.objects.filter(teacher=teacher_profile)
    schedules = Schedule.objects.filter(class_instance__in=[a.class_assigned for a in assigned_classes])

    return render(request, 'teacher_dashboard.html', {
        'teacher_profile': teacher_profile,
        'assigned_classes': assigned_classes,
        'schedules': schedules,
    })

@login_required
def student_dashboard(request):
    user = request.user
    student_profile = StudentProfile.objects.get(user=user)
    
    # Get active academic year
    active_academic_year = AcademicYear.objects.filter(is_active=True).first()
    
    # Enrollments for the active academic year
    enrollments = StudentEnrollment.objects.filter(student=student_profile, academic_year=active_academic_year)
    
    # Attendance records for the active academic year
    attendance_records = Attendance.objects.filter(student=student_profile, academic_year=active_academic_year)
    
    # Exams and exam grades for the active academic year
    exam_grades = ExamGrade.objects.filter(student=student_profile, academic_year=active_academic_year)
    
    # Class details for the active academic year
    class_instance = enrollments.first().class_assigned if enrollments.exists() else None
    
    # Schedule for the student's class in the active academic year
    schedule = Schedule.objects.filter(class_instance=class_instance)
    
    # Notifications targeting the student’s class or grade in the active academic year
    notifications = Notification.objects.filter(
        is_active=True,
        scope__in=['Class', 'Grade', 'School']
    ).filter(
        class_target=class_instance  # For class-specific notifications
    ) | Notification.objects.filter(
        grade_target=class_instance.grade  # For grade-specific notifications
    ) | Notification.objects.filter(
        scope='School'  # For school-wide notifications
    ).distinct()

    return render(request, 'student_dashboard.html', {
        'student_profile': student_profile,
        'enrollments': enrollments,
        'attendance_records': attendance_records,
        'exam_grades': exam_grades,
        'class_instance': class_instance,
        'schedule': schedule,
        'notifications': notifications,
    })

def parent_dashboard(request):
    user = request.user
    parent_profile = ParentProfile.objects.get(user=user)
    children = parent_profile.students.all()

    return render(request, 'parent_dashboard.html', {
        'parent_profile': parent_profile,
        'children': children,
    })



