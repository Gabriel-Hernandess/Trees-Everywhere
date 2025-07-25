from django.urls import path
from .views import MyTreesView, GroupsTrees, MyProfile

urlpatterns = [
    path('planted-trees/', MyTreesView.as_view(), name='planted-trees'),
    path('group-trees/', GroupsTrees.as_view(), name='group-trees'),
    path('my-profile/', MyProfile.as_view(), name='my-profile'),
]