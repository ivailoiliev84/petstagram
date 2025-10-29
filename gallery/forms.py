from django import forms
from gallery.models import Post




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
