from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Student URLs
    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/book-slot/', views.BookSlotView.as_view(), name='book_slot'),
    path('student/update-project/', views.UpdateProjectView.as_view(), name='update_project'),

    # Mentor URLs
    path('mentor/dashboard/', views.MentorDashboardView.as_view(), name='mentor_dashboard'),
    path('mentor/create-slot/', views.CreateSlotView.as_view(), name='create_slot'),
    path('mentor/accept-booking/<int:pk>/', views.AcceptBookingView.as_view(), name='accept_booking'),
    path('mentor/reject-booking/<int:pk>/', views.RejectBookingView.as_view(), name='reject_booking'),
] 