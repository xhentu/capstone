from django.contrib import admin
from .models import (
    AcademicYear,
    Class,
    Subject,
    TeacherAssignment,
    Schedule,
    StudentEnrollment,
    Attendance,
    Exam,
    ExamGrade,
    Fees,
    Grade,
    Notification,  # Include the Notification model in admin
    TeacherDailyAttendance,
    StaffDailyAttendance,
)

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_active')
    search_fields = ('year',)
    list_filter = ('is_active',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'academic_year', 'is_active')
    list_filter = ('grade', 'academic_year', 'is_active')
    search_fields = ('name', 'grade__name', 'academic_year__year')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'academic_year', 'is_active')
    list_filter = ('grade', 'academic_year', 'is_active')
    search_fields = ('name', 'grade__name', 'academic_year__year')
    filter_horizontal = ('classes',)

    def save_model(self, request, obj, form, change):
        # Save the subject instance first
        obj.save()
        
        # Now handle the many-to-many relationship
        classes = form.cleaned_data.get('classes', [])
        obj.classes.set(classes)

@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'class_assigned', 'academic_year')
    list_filter = ('academic_year', 'class_assigned__is_active')
    search_fields = ('teacher__user__username', 'subject__name', 'class_assigned__name', 'academic_year__year')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'class_instance', 'get_academic_year', 'day_of_week', 'section')
    list_filter = ('class_instance__academic_year', 'day_of_week', 'section')  # Added section filter for time slots
    search_fields = ('subject__name', 'class_instance__name', 'class_instance__academic_year__year')

    def get_academic_year(self, obj):
        return obj.class_instance.academic_year.year
    get_academic_year.short_description = 'Academic Year'

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_assigned', 'academic_year')
    list_filter = ('academic_year', 'class_assigned__is_active')
    search_fields = ('student__user__username', 'class_assigned__name', 'academic_year__year')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'academic_year')
    list_filter = ('academic_year', 'status')
    search_fields = ('student__user__username', 'subject__name', 'academic_year__year')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'class_assigned', 'exam_date', 'academic_year')
    list_filter = ('academic_year', 'exam_date', 'class_assigned__is_active')
    search_fields = ('name', 'subject__name', 'class_assigned__name', 'academic_year__year')

@admin.register(ExamGrade)
class ExamGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'grade', 'academic_year')
    list_filter = ('academic_year', 'grade')
    search_fields = ('student__user__username', 'exam__name', 'academic_year__year')

@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_due', 'amount_paid', 'due_date', 'academic_year', 'fee_status')
    list_filter = ('academic_year', 'due_date', 'amount_paid')
    search_fields = ('student__user__username', 'academic_year__year')

    @admin.display(description='Fee Status')
    def fee_status(self, obj):
        return obj.fee_status

# Adding Notification to admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'scope', 'sender', 'created_at', 'is_active')
    list_filter = ('scope', 'is_active', 'created_at')
    search_fields = ('title', 'sender__user__username')

    def save_model(self, request, obj, form, change):
        # Ensure proper validation and saving for the scope targeting
        obj.save()

        if obj.scope == 'Class':
            classes = form.cleaned_data.get('class_target', [])
            obj.class_target.set(classes)

        if obj.scope == 'Grade':
            grades = form.cleaned_data.get('grade_target', [])
            obj.grade_target.set(grades)

@admin.register(TeacherDailyAttendance)
class TeacherDailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('teacher__user__username',)
    date_hierarchy = 'date'

    def get_ordering(self, request):
        return ['-date']

@admin.register(StaffDailyAttendance)
class StaffDailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('staff__user__username',)
    date_hierarchy = 'date'

    def get_ordering(self, request):
        return ['-date']
    
