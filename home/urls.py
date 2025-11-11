from django.urls import path
from home.views import HomeView, ExploreView, ContactView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('contact/', ContactView.as_view(), name='contact'),
    
]