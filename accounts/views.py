from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserCreationForm, UserLoginForm
# Create your views here.

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
    
 
class UserProfileView(LoginRequiredMixin, View):
     
     def get(self, request):
        return render(request, 'accounts/profile.html')
     