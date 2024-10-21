from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# CustomUser model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Add related_name to avoid conflict with auth.User reverse accessors
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

# Profile model for Admin
class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Admin)'

# Profile model for Staff
class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Staff)'

# Profile model for Teachers
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Teacher)'

# Profile model for Students
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Student)'

# Profile model for Parents
class ParentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.username} (Parent)'
