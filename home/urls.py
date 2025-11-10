from django.urls import path
from home.views import HomeView, ExploreView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('explore', ExploreView.as_view(), name='explore'),
]