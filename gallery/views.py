from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from gallery.forms import CreatePostForm
from gallery.models import Post
# Create your views here.

class Gallery(LoginRequiredMixin, View):
    
    gallery_template = "gallery/gallery_main.html"

    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, self.gallery_template, context)
    
class CreatePost(LoginRequiredMixin, View):
    create_post_template = 'gallery/create_post.html'

    def get(self, request):
        form = CreatePostForm(request.POST, )
        return render(request, self.create_post_template, {'form': form})
    
    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('gallery')
        context = {'form': form}
        return render(request, self.create_post_template, context)
