from django.urls import include
from django.urls import path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("auth/", include("authentication.urls")),
    path("bookings/", include("booking.urls")),
    path("doctor-notes/", include("doctorsnote.urls")),
    path("actionable-steps/", include("actionable_steps.urls")),






]
