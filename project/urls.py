from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('apps.management.urls')),
    path('', include('apps.users.urls')),
    path('trees/', include('apps.trees.urls')),
]