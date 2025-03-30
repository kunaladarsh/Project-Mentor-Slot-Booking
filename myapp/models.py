from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('mentor', 'Mentor'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    sap_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()
    passing_year = models.IntegerField()
    project_title = models.CharField(max_length=200, blank=True)
    project_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office_number = models.CharField(max_length=20)
    total_slots = models.IntegerField(default=0)
    filled_slots = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.office_number}"

    def has_available_slots(self):
        return self.filled_slots < self.total_slots

class Slot(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['mentor', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.mentor.user.username} - {self.date} {self.start_time}-{self.end_time}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'slot']

    def __str__(self):
        return f"{self.student.user.username} - {self.slot} - {self.status}"

    def accept(self):
        if self.status == 'pending':
            self.status = 'accepted'
            self.slot.is_available = False
            self.slot.mentor.filled_slots += 1
            self.slot.mentor.save()
            self.slot.save()
            self.save()
            return True
        return False

    def reject(self):
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()
            return True
        return False
