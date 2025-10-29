from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class Gallery(LoginRequiredMixin, View):
    
    gallery_template = "gallery/gallery.html"

    def get(self, request):
        return render(request, self.gallery_template)
    
