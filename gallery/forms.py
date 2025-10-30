from django import forms
from gallery.models import Post, PostComment


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'description', 'image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide help text, add classes/placeholders, etc.
        for _,field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update({
                "class": "form-control",  # 👈 Bootstrap style
                "placeholder": field.label,
            })


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={  # single-line input; use Textarea if you prefer
                'placeholder': 'Write a comment...',
                'class': 'form-control',
            })
        }
