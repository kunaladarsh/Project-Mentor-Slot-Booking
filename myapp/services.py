from django.db import transaction
from django.utils import timezone
from .models import Student, Mentor, Slot, Booking
from datetime import datetime, date

class SlotBookingService:
    @staticmethod
    def create_slot(mentor, date, start_time, end_time):
        """Create a new slot for a mentor"""
        return Slot.objects.create(
            mentor=mentor,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

    @staticmethod
    def get_available_slots(mentor, date=None):
        """Get all available slots for a mentor"""
        query = {'mentor': mentor, 'is_available': True}
        if date:
            query['date'] = date
        return Slot.objects.filter(**query)

    @staticmethod
    @transaction.atomic
    def book_slot(student, slot):
        """Book a slot for a student"""
        if not slot.is_available:
            return None, "Slot is not available"
        
        if not slot.mentor.has_available_slots():
            return None, "Mentor has no available slots"

        booking = Booking.objects.create(
            student=student,
            slot=slot,
            status='pending'
        )
        return booking, "Booking request created successfully"

class MentorService:
    @staticmethod
    def update_slot_availability(mentor, total_slots):
        """Update mentor's total slots"""
        mentor.total_slots = total_slots
        mentor.save()
        return mentor

    @staticmethod
    def get_pending_requests(mentor):
        """Get all pending booking requests for a mentor"""
        return Booking.objects.filter(
            slot__mentor=mentor,
            status='pending'
        ).select_related('student', 'slot')

class StudentService:
    @staticmethod
    def get_student_bookings(student):
        """Get all bookings for a student"""
        return Booking.objects.filter(
            student=student
        ).select_related('slot', 'slot__mentor')

    @staticmethod
    def update_project_details(student, project_title, project_description):
        """Update student's project details"""
        student.project_title = project_title
        student.project_description = project_description
        student.save()
        return student 