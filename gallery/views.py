from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count, OuterRef
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from gallery.forms import CreatePostForm, CommentForm
from gallery.models import Post, PostComment, PostLike, PostDislike
# Create your views here.



class Gallery(LoginRequiredMixin, View):
    
    gallery_template = "gallery/gallery_main.html"

    def get(self, request):
        # posts = Post.objects.all()
   
        posts= (
            Post.objects.select_related('user')
            .annotate(
               comments_count = Count('comments', distinct=True),
               likes_count = Count('likes', distinct=True),
               dislikes_count = Count('dislikes', distinct=True)
            )
        )
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
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()

        comments = post.comments.select_related('user', 'user__userprofile').order_by('-created_at')
        likes_count = PostLike.objects.filter(post=post).count()
        context = {'form':form, 
                   'post': post, 
                   'comments': comments,
                   'likes_count': likes_count
                   }
        
        return render(request, self.post_details_template, context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_details', pk=post.id)
        comments = post.comments.select_related('user').order_by('-created_at')
        return render(request, self.post_details_template, {'form':form, 'post': post, 'comments': comments})

class EditPost(LoginRequiredMixin, View):
    edit_post_template = 'gallery/edit_post.html'
     
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CreatePostForm(instance=post)
        return render(request, self.edit_post_template, {'form':form, 'post':post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', pk=post.pk)
        return render(request, self.edit_post_template, {'form': form, 'post': post})
    

class DeleteComment(LoginRequiredMixin, View):

    def get(self, request, pk):
        comment = get_object_or_404(PostComment, pk=pk)
        post = get_object_or_404(Post, pk=comment.post.pk)
        comment.delete()
        return redirect('post_details', pk=post.pk)
        
        
class DeletePost(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('gallery')


class PostLikeView(LoginRequiredMixin, View):

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        like_qs = PostLike.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs.delete()
        else:
            PostLike.objects.create(user=request.user, post=post)
            PostDislike.objects.filter(user=request.user, post=post).delete()
        return redirect('gallery')
   

class PostDislikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        dislike_qs = PostDislike.objects.filter(user=request.user, post=post)

        if dislike_qs.exists():
            dislike_qs.delete()
        else:
            PostDislike.objects.create(user=request.user, post=post)
            PostLike.objects.filter(user=request.user, post=post).delete()

        return redirect('gallery')
    