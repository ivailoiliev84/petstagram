from django.urls import path
from accounts.views import UserRegisterView, UserLoginView, UserLogoutView, UserProfileDetailsView, UserProfileEditView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UserProfileDetailsView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', UserProfileEditView.as_view(), name='profile_edit'),
]
