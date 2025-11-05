from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(cache_page(60 * 5), name='dispatch')   # 5 minutes
class HomeView(View):

    def get(self, request):
        user = request.user
        print(user.is_authenticated)
        return render(request, 'home/home.html', {'user': user})
    