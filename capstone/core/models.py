from django.db import models
from django.core.exceptions import ValidationError


class AcademicYear(models.Model):
    year = models.CharField(max_length=20, blank=True, null=True)  # Example: "2024-2025"
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.year

    def save(self, *args, **kwargs):
        # If this academic year is set to active, deactivate all others
        if self.is_active:
            # Set all other academic years' is_active to False
            AcademicYear.objects.exclude(id=self.id).update(is_active=False)
        
        # Call the original save method to save this instance
        super(AcademicYear, self).save(*args, **kwargs)

class Grade(models.Model):
    name = models.CharField(max_length=20)  # Example: "Grade 1", "Grade 2", etc.

    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)  # Example: "Class A"
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.grade.name} - {self.academic_year.year}"

class Subject(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)  # Example: "Mathematics"
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)  # Subject's grade
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)
    classes = models.ManyToManyField(Class, blank=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.grade.name} - {self.academic_year.year}"

    def clean(self):
        # Ensure that the subject is only associated with classes of the same grade
        # (but defer this validation until the instance has been saved).
        pass  # Move this logic to the save method
    
    def save(self, *args, **kwargs):
        # First save the subject to ensure it has an ID and is stored in the database
        super().save(*args, **kwargs)
        
        # Now validate the classes associated with this subject
        for class_instance in self.classes.all():
            if class_instance.grade != self.grade:
                raise ValidationError(
                    f"Cannot assign {self.name} (Grade {self.grade.name}) to {class_instance.name} (Grade {class_instance.grade.name}). "
                    "The subject grade must match the class grade."
                )
        
        # If validation passes, save the subject again (if necessary)
        super().save(*args, **kwargs)

# Schedule Model
class Schedule(models.Model):
    SECTION_CHOICES = [
        ('1st Section', '9:00 am - 10:30 am'),
        ('2nd Section', '10:45 am - 12:15 pm'),
        ('Break', '12:15 pm - 12:45 pm'),  # 30-minute break
        ('3rd Section', '12:45 pm - 1:15 pm'),
        ('4th Section', '2:00 pm - 3:30 pm'),
    ]

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="timetable")
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name="scheduled_sections")
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)

    def __str__(self):
        return f"{self.class_instance.name} - {self.section} ({self.day_of_week}) - {self.subject.name if self.subject else 'No Subject'}"

# Teacher Assignment Model
class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.teacher.user.username} teaches {self.subject.name} in {self.class_assigned.name} ({self.academic_year.year})"
    
    def clean(self):
        if not self.class_assigned.is_active:
            raise ValidationError(f"Cannot assign teacher to an inactive class: {self.class_assigned.name}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# Student Enrollment Model
class StudentEnrollment(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} in {self.class_assigned.name} ({self.academic_year.year})"
    
    def clean(self):
        if not self.class_assigned.is_active:
            raise ValidationError(f"Cannot enroll student in an inactive class: {self.class_assigned.name}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# Attendance Model
class Attendance(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.date} ({self.status})"

class Exam(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # Example: "Mid-term Exam"
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.subject.name} - {self.class_assigned.name} ({self.academic_year.year})"

class ExamGrade(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Example: 95.50
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.exam.name} - {self.subject.name} ({self.grade})"

class Fees(models.Model):
    student = models.ForeignKey('users.StudentProfile', on_delete=models.CASCADE, blank=True, null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - Due: {self.amount_due}, Paid: {self.amount_paid}"

    @property
    def fee_status(self):
        if self.amount_paid == self.amount_due:
            return "Complete"
        elif self.amount_paid > 0 and self.amount_paid < self.amount_due:
            return "Partially Paid"
        else:
            return "Not Paid"
        
class Notification(models.Model):
    SCOPE_CHOICES = [
        ('Class', 'Specific Class'),
        ('Grade', 'Grade-level Classes'),
        ('School', 'Entire School'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    sender = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE)  # Assuming StaffProfile includes admin, staff, teachers
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default='School')
    
    class_target = models.ManyToManyField(Class, blank=True)  # For 'Class' scope
    grade_target = models.ManyToManyField(Grade, blank=True)  # For 'Grade' scope
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.sender.user.username}"

    def clean(self):
        # Ensure targeting logic is valid based on scope
        if self.scope == 'Class' and not self.class_target.exists():
            raise ValidationError("Please select at least one class when targeting specific classes.")
        if self.scope == 'Grade' and not self.grade_target.exists():
            raise ValidationError("Please select at least one grade when targeting grade-level classes.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class TeacherDailyAttendance(models.Model):
    date = models.DateField()
    teacher = models.ForeignKey('users.TeacherProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], blank=True, null=True)

    class Meta:
        unique_together = ('date', 'teacher')  # Ensures a teacher can't have multiple attendance records for the same day

    def __str__(self):
        return f"{self.teacher.user.username} - {self.date} ({self.status})"
    
class StaffDailyAttendance(models.Model):
    date = models.DateField()
    staff = models.ForeignKey('users.StaffProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')], blank=True, null=True)

    class Meta:
        unique_together = ('date', 'staff')  # Ensures a staff member can't have multiple attendance records for the same day

    def __str__(self):
        return f"{self.staff.user.username} - {self.date} ({self.status})"

