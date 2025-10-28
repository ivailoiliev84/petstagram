from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(field_name)
            print(field)
            field.widget.attrs['class'] = 'form-control'    


        # Force 'description' to use Textarea with 3 rows
        self.fields['description'].widget = forms.Textarea(
            attrs={
                'class': self.fields['description'].widget.attrs.get('class', 'form-control'),
                'rows': 3,  # 👈 override 10
                'cols': 40,  # optional
            }
        )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
