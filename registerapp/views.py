from django.shortcuts import render

# Create your views here.

from django.contrib import messages, auth
from .models import Profile
from django.contrib.auth.decorators import login_required  # Import login_required decorator if not imported already
from django.shortcuts import render, redirect
from .forms import  UserUpdateForm
from django.contrib.auth.models import User



# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return redirect(request,"login.html")
    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password1')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password,
                                                first_name=first_name, last_name=last_name, email=email)
                user.save()

                Profile.objects.create(user=user)

                messages.success(request, 'Account created successfully. You can now log in.')
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")
    return render(request, "register.html")

def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)


        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)


    return render(request, 'profile_update.html', {'user_form': user_form})
