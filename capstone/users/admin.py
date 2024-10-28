from django.contrib import admin
from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, SalaryPayment, StudentProfile, ParentProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'nrc_no', 'gender', 'religion']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'nrc_no']
    list_filter = ['role', 'gender', 'religion']

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'salary']
    search_fields = ['user__username']
    
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'salary']
    search_fields = ['user__username']

class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'payment_date', 'amount_paid', 'notes']
    search_fields = ['profile__username', 'notes']
    list_filter = ['payment_date']

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AdminProfile, AdminProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(SalaryPayment, SalaryPaymentAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(ParentProfile, ParentProfileAdmin)
