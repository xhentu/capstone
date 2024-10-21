from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AdminProfile, StaffProfile, TeacherProfile, StudentProfile, ParentProfile

# Signal to create a profile and assign the user to the appropriate group upon user creation
@receiver(post_save, sender=CustomUser)
def create_profile_and_assign_group(sender, instance, created, **kwargs):
    if created:
        print(f"User {instance.username} created with role {instance.role}")
        
        # Create profile based on role
        if instance.role == 'admin':
            AdminProfile.objects.create(user=instance)
            print(f"Admin profile created for {instance.username}")
            admin_group, _ = Group.objects.get_or_create(name='Admin')
            instance.groups.add(admin_group)

        elif instance.role == 'staff':
            StaffProfile.objects.create(user=instance)
            print(f"Staff profile created for {instance.username}")
            staff_group, _ = Group.objects.get_or_create(name='Staff')
            instance.groups.add(staff_group)

        elif instance.role == 'teacher':
            TeacherProfile.objects.create(user=instance)
            print(f"Teacher profile created for {instance.username}")
            teacher_group, _ = Group.objects.get_or_create(name='Teacher')
            instance.groups.add(teacher_group)

        elif instance.role == 'student':
            StudentProfile.objects.create(user=instance)
            print(f"Student profile created for {instance.username}")
            student_group, _ = Group.objects.get_or_create(name='Student')
            instance.groups.add(student_group)

        elif instance.role == 'parent':
            ParentProfile.objects.create(user=instance)
            print(f"Parent profile created for {instance.username}")
            parent_group, _ = Group.objects.get_or_create(name='Parent')
            instance.groups.add(parent_group)
