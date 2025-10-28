from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from accounts.forms import UserCreationForm, UserLoginForm, EditUserProfileForm, CustomPasswordChangeForm
from accounts.models import UserProfile
from django.contrib.auth import get_user_model
# Create your views here.

AppUser = get_user_model()

class UserRegisterView(View):
    
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user}!")
            return redirect("login")  # or wherever you want to redirect
        else:
            # if form is invalid, re-render the form with error messages
            return render(request, "accounts/register.html", {"form": form})
        

class UserLoginView(View):

    def get(self, request):
        form = UserLoginForm()
        return  render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/login.html', {'form': form})
    

class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('home')
    
 
class UserProfileDetailsView(LoginRequiredMixin, View):
    profile_details_template = "accounts/profile.html"
    
    def get(self, request, pk):
        profile = UserProfile.objects.get(user_id=pk)
        context = {'profile': profile}
        return render(request, self.profile_details_template, context)
     

class UserProfileEditView(LoginRequiredMixin, View):

    
    profile_details_template = 'accounts/profile_edit.html'

    def get(self, request, pk):
        profile = UserProfile.objects.get(user_id=pk)
        form = EditUserProfileForm(instance=profile)
        return render(request, self.profile_details_template, {'form': form})
    
    def post(self, request, pk):
        profile = UserProfile.objects.get(user_id=pk)
        form = EditUserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('profile', pk=pk)
        return redirect(request, self.profile_details_template, {'profile': profile})

class ChangePasswordView(PasswordChangeView):
    
    form_class = CustomPasswordChangeForm
    template_name = "accounts/change_password.html"

    def get_success_url(self):
     
        return reverse_lazy("profile", kwargs={"pk": self.request.user.id})
    