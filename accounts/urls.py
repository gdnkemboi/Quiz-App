from django.urls import path
from .views import UserProfileView, ProfileUpdateView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("<int:pk>/profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]
