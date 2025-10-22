from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeView(View):

    def get(self, request):
        user = request.user
        print(user.is_authenticated)
        return render(request, 'home/home.html', {'user': user})
    
