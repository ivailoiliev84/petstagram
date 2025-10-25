from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from accounts.models import UserProfile

User = get_user_model()

class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

        
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "you@example.com",
                "class": "input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide help text, add classes/placeholders, etc.
        for _,field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update({
                "class": "form-control",  # 👈 Bootstrap style
                "placeholder": field.label,
            })


class UserLoginForm(forms.Form):
    email = forms.CharField(
        label="Email", 
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "email"})
    )
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"})
    )
    remember_me = forms.BooleanField(required=False, initial=False)

    def clean(self):
        cleaned = super().clean()
        e, p = cleaned.get("email"), cleaned.get("password")
        if not e or not p:
            return cleaned
        user = authenticate(username=e, password=p)
        if not user:
            raise forms.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        self.user = user  # store for the view
        return cleaned

    def get_user(self):
        return getattr(self, "user", None)
    

class EditUserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ("user",)
