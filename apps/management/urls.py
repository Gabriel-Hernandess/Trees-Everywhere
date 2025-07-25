from django.urls import path

from .views import RegisterView, AdminAccountsView, AdminTreesView, AdminUsersView

urlpatterns = [
    path('accounts/', AdminAccountsView.as_view(), name='admin-accounts'),
    path('users/', AdminUsersView.as_view(), name='admin-users'),
    path('trees/', AdminTreesView.as_view(), name='admin-trees'),

    path('register/', RegisterView.as_view(), name="register"),
]