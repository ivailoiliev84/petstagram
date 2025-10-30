from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
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
        form = CreatePostForm()
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



class PostDetails(LoginRequiredMixin, View):
    post_details_template = 'gallery/post_details.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, self.post_details_template, {'post': post})



class EditPost(LoginRequiredMixin, View):
    edit_post_template = 'gallery/edit_post.html'
     
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CreatePostForm(instance=post)
        return render(request, self.edit_post_template, {'form':form, 'post':post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CreatePostForm(request.POST, request.FILES, instance=post)  # ✅ important
        if form.is_valid():
            form.save()
            return redirect('post_details', pk=post.pk)
        return render(request, self.edit_post_template, {'form': form, 'post': post})