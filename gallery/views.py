from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from gallery.forms import CreatePostForm, CommentForm
from gallery.models import Post, PostComment, PostLike, PostDislike
from gallery.services.moderation import moderate_form

# Create your views here.

class Gallery(LoginRequiredMixin, View):
    
    gallery_template = "gallery/gallery_main.html"

    def get(self, request):
        posts= (
            Post.objects.select_related('user', 'user__userprofile')
            .annotate(
               comments_count = Count('comments', distinct=True),
               likes_count = Count('likes', distinct=True),
               dislikes_count = Count('dislikes', distinct=True)
            )
            .order_by("-created_at")
        )
        
        paginator = Paginator(posts, 6)  # 6 posts per page

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        context = {
            'posts': page_obj,
            'page_obj': page_obj,
        }

        return render(request, self.gallery_template, context)

    
class CreatePost(LoginRequiredMixin, View):
    create_post_template = 'gallery/create_post.html'

    def get(self, request):
        form = CreatePostForm()
        return render(request, self.create_post_template, {'form': form})
    
    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid() and moderate_form(form):
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('gallery')
        context = {'form': form}
        return render(request, self.create_post_template, context)

class PostDetails(LoginRequiredMixin, View):
    template_name = 'gallery/post_details.html'

    def get_post(self, pk):
        qs = (
            Post.objects.select_related('user')
            .annotate(
                likes_count=Count('likes', distinct=True),
                dislikes_count=Count('dislikes', distinct=True),
                comments_count=Count('comments', distinct=True),
            )
        )
        return get_object_or_404(qs, pk=pk)

    def render_page(self, request, post, form):
        comments = (
            post.comments
            .select_related('user', 'user__userprofile')
            .order_by('-created_at')
        )

        return render(request, self.template_name, {
            'post': post,
            'comments': comments,
            'form': form,
        })

    def get(self, request, pk):
        post = self.get_post(pk)
        return self.render_page(request, post, CommentForm())

    def post(self, request, pk):
        post = self.get_post(pk)
        form = CommentForm(request.POST)

        if form.is_valid() and moderate_form(form):
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            return redirect('post_details', pk=post.pk)

        return self.render_page(request, post, form)

class EditPost(LoginRequiredMixin, View):
    edit_post_template = 'gallery/edit_post.html'
     
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        form = CreatePostForm(instance=post)
        return render(request, self.edit_post_template, {'form':form, 'post':post})
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid() and moderate_form(form, changed_only=True):
            form.save()
            return redirect('post_details', pk=post.pk)
        return render(request, self.edit_post_template, {'form': form, 'post': post})
    

class EditCommentView(LoginRequiredMixin, View):
    edit_comment_template = 'gallery/edit_comment.html'

    def get(self, request, pk):
        comment = get_object_or_404(
            PostComment.objects.select_related('post', 'user'),
            pk=pk,
            user=request.user
        )

        form = CommentForm(instance=comment)

        context = {
            'form': form,
            'post': comment.post,
            'comment': comment,
        }

        return render(request, self.edit_comment_template, context)

    def post(self, request, pk):
        comment = get_object_or_404(
            PostComment.objects.select_related('post', 'user'),
            pk=pk,
            user=request.user
        )

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid() and moderate_form(form, changed_only=True):
            form.save()
            return redirect('post_details', pk=comment.post_id)

        context = {
            'form': form,
            'post': comment.post,
            'comment': comment,
        }

        return render(request, self.edit_comment_template, context)     

class DeletePost(LoginRequiredMixin, View):
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        post.delete()
        return redirect('gallery')
    
class DeleteComment(LoginRequiredMixin, View):

    def post(self, request, pk):
        comment = get_object_or_404(
            PostComment,
            pk=pk,
            user=request.user
        )

        post_id = comment.post_id
        comment.delete()

        return redirect('post_details', pk=post_id)


class PostLikeView(LoginRequiredMixin, View):

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like_qs = PostLike.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs.delete()
        else:
            PostLike.objects.create(user=request.user, post=post)
            PostDislike.objects.filter(user=request.user, post=post).delete()
        return redirect('gallery')
   

class PostDislikeView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        dislike_qs = PostDislike.objects.filter(user=request.user, post=post)

        if dislike_qs.exists():
            dislike_qs.delete()
        else:
            PostDislike.objects.create(user=request.user, post=post)
            PostLike.objects.filter(user=request.user, post=post).delete()

        return redirect('gallery')
    