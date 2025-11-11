from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.


class HomeView(View):
    home_template = 'home/home.html'
    
    def get(self, request):
        user = request.user
        return render(request, self.home_template, {'user': user})
    
@method_decorator(cache_page(60 * 5), name='dispatch')   # 5 minutes
class ExploreView(View):
    explore_template = 'home/explore.html'
    
    def get(self, request):
        
        return render(request, self.explore_template)
    
    
class ContactView(View):
    contact_us_template = 'home/contact_us.html'
    
    def get(self, request):
        
        return render(request, self.contact_us_template)