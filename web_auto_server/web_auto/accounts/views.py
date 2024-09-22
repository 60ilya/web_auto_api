from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('')
    

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
