from django.urls import path

from .views import IndexView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name="login"),
]