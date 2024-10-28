from django.contrib import admin
from .models import AcademicYear, Grade, Class, Subject, Schedule, TeacherAssignment, StudentEnrollment, Attendance, Exam, ExamGrade, Fees, Notification, TeacherDailyAttendance, StaffDailyAttendance

class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year', 'is_active']
    search_fields = ['year']

class GradeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'academic_year', 'is_active']
    search_fields = ['name']
    list_filter = ['grade', 'academic_year', 'is_active']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'academic_year', 'is_active']
    search_fields = ['name']
    list_filter = ['grade', 'academic_year', 'is_active']

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['class_instance', 'section', 'subject', 'day_of_week']
    search_fields = ['class_instance__name', 'subject__name']
    list_filter = ['day_of_week']

class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'subject', 'class_assigned', 'academic_year']
    search_fields = ['teacher__user__username', 'subject__name']
    list_filter = ['academic_year']

class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_assigned', 'academic_year']
    search_fields = ['student__user__username']
    list_filter = ['academic_year']

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'date', 'status', 'academic_year']
    search_fields = ['student__user__username', 'subject__name']
    list_filter = ['date', 'status']

class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'class_assigned', 'exam_date', 'academic_year']
    search_fields = ['name', 'subject__name']
    list_filter = ['exam_date', 'academic_year']

class ExamGradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'subject', 'grade', 'academic_year']
    search_fields = ['student__user__username', 'exam__name', 'subject__name']
    list_filter = ['academic_year']

class FeesAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount_due', 'amount_paid', 'due_date', 'fee_status', 'academic_year']
    search_fields = ['student__user__username']
    list_filter = ['academic_year']

    def fee_status(self, obj):
        return obj.fee_status
    fee_status.admin_order_field = 'fee_status'

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'sender', 'scope', 'is_active', 'created_at']
    search_fields = ['title', 'message']
    list_filter = ['scope', 'is_active']

class TeacherDailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'teacher', 'status']
    search_fields = ['teacher__user__username']
    list_filter = ['date', 'status']

class StaffDailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ['date', 'staff', 'status']
    search_fields = ['staff__user__username']
    list_filter = ['date', 'status']

# Register models
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(TeacherAssignment, TeacherAssignmentAdmin)
admin.site.register(StudentEnrollment, StudentEnrollmentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamGrade, ExamGradeAdmin)
admin.site.register(Fees, FeesAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(TeacherDailyAttendance, TeacherDailyAttendanceAdmin)
admin.site.register(StaffDailyAttendance, StaffDailyAttendanceAdmin)
