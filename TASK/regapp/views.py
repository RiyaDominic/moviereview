
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('regapp:register')
        # Check if the username is available
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username is not available")
            return redirect('regapp:register')
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered")
            return redirect('regapp:register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Registration successful.")
        return redirect('regapp:login')

    return render(request, 'register.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password= request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/app/')
        else:
            messages.info(request,"invalid username or password")
            return redirect('regapp:login')
    return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/app/')


def view_profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})



def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        # Extract form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        
        # Update user information
        if username:
            user.username = username
        if email:
            user.email = email
        if new_password:
            # Only set password if user is not anonymous
            user.set_password(new_password)

        # Save the updated user information
            user=user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('regapp:login')  # Redirect to the profile page
    return render(request, 'editprofile.html', {'user': user})