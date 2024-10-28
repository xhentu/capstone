from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    RELIGION_CHOICES = [
        ('islam', 'Islam'),
        ('christianity', 'Christianity'),
        ('hinduism', 'Hinduism'),
        ('buddhism', 'Buddhism'),
        ('none', 'None'),
        ('other', 'Other'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    nrc_no = models.CharField(max_length=50, blank=True, null=True)  # NRC/ID number
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # Physical address
    email = models.EmailField(blank=True, null=True)  # Overriding or additional
    date_of_birth = models.DateField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Custom related_name to resolve the clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom related_name to resolve the clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

# Profile model for Admin
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Admin)'

class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Monthly Salary
    def __str__(self):
        return f'{self.user.username} (Staff)'

class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Monthly Salary
    def __str__(self):
        return f'{self.user.username} (Teacher)'

class SalaryPayment(models.Model):
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Could be Staff or Teacher
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)  # Optional notes about the payment

    def __str__(self):
        return f'{self.profile.username} - {self.payment_date} - {self.amount_paid}'

# Profile model for Students
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Student)'

class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(StudentProfile, blank=True, related_name="parents")
    def __str__(self):
        return f'{self.user.username} (Parent)'

