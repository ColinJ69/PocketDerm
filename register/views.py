from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
 
            
            login(request, user)

            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


    
