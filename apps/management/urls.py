from django.urls import path

from .views import RegisterView, AdminDashboardView

urlpatterns = [
    path('management/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('register/', RegisterView.as_view(), name="register"),
]