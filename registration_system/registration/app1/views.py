from django.http import HttpResponse
from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import person_collection
from django.http import JsonResponse
import json
from bson import ObjectId 
@login_required(login_url='login')
def home(request):
    return render (request,'home.html') 

def user_profile(request):
    return render (request,'user_profile.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # Check if passwords match
        if pass1 != pass2:
            return render(request, "signup.html", {'msg': ['Passwords do not match']}) 
        else:
            # Create user
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.is_active = False
            my_user.save()
            return render(request, "signup.html", {'msg1': ['Account created, please wait for the expert verification']}) 
        
    else:
        # Return a default response if the request method is not POST
        return render(request, 'signup.html')
    


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if(user.is_superuser):
                return redirect('account')  # Redirect to the 'accounts' page upon successful login
            else:
                return redirect('dashboard_user') 
        else:
            return render(request, "login.html", {'msg2': ['Watch Out ! Username or Password incorrect.']}) 
    
    return render(request, 'login.html')  # Render the login page template for GET requests




def dashboard(request):
    return render(request,'dashboard.html')

def account(request):
    users = User.objects.all()
    return render(request,'account.html',{'users': users})

def user_dash(request):
    users = User.objects.all()
    return render(request, 'dashboard_user.html', {'users': users})

def Deleteuser(request,pk):
    uname=User.objects.get(pk=pk)
    b=User.objects.filter(username=uname)
    b.delete()
    # Add a success message
    messages.success(request, 'User account has been successfully deleted.')
    return redirect('account')

def update(request,pk):
    user=User.objects.get(pk=pk)
    return render(request,'update.html',{'user':user})

def updateuser(request, pk):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        user = User.objects.get(pk=pk)
        user.first_name = fname
        user.last_name = lname
        user.username = name
        user.email = email
        user.save()
        # Add a success message
        messages.success(request, 'User account has been successfully updated.')
        return redirect('account')

def updatprofile(request, pk):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        user = User.objects.get(pk=pk)
        user.first_name = fname
        user.last_name = lname
        user.username = name
        user.email = email
        user.save()
        # Add a success message
        messages.success(request, 'User account has been successfully updated.')
        return redirect('user_profile')

def AddUser(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        # Check if passwords match
        if pass1 != pass2:
            return HttpResponse("Passwords do not match")
        else :
            # Create user
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.is_active=False
            my_user.save()
            # Add a success message
            messages.success(request, 'User account has been successfully added.')
            return redirect('account') #use the name from views.py
    else :
        # Return a default response if the request method is not POST
        return render(request,'add_user.html')  

def verify_user(request, pk):
    # Check if the logged-in user is an admin
    if request.user.is_superuser:
        try:
            # Retrieve the user object by ID
            user = User.objects.get(pk=pk)
            if not user.is_active:  # Check if user is not already active
                # Update user permissions to grant access to log in
                user.is_active = True
            
                # Email sender
                subject = "Account Verification" 
                message = f"Dear {user.username}, your account has been verified now. You are now able to access your account."
                email = user.email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True) 
                # Save user
                user.save()
                # Add a success message for verification
                messages.success(request, 'User account has been successfully verified.')
            else:
                # Update user permissions to revoke access
                user.is_active = False
                # Add a success message for unverification
                messages.success(request, 'User account has been unverified.')
            user.save()  # Save user changes

        except User.DoesNotExist:
            # Handle case where user does not exist
            messages.error(request, 'User does not exist.')
    else:
        # Return unauthorized access message
        messages.error(request, 'Unauthorized access.')

    return redirect('account')  # Redirect admin to admin dashboard after verification






def index(request):
    return HttpResponse("<h1>app is runnning</h1>")


def add_person(request):
    records={
        "first_name":"john",
        "last_name":"smith"
    }

    person_collection.insert_one(records)
    return HttpResponse("new person is added")

def convert_to_json(obj):
    """Converts ObjectId to string for JSON serialization."""
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def get_all_person(request):
    persons = list(person_collection.find())
    # Convert MongoDB cursor to a list of dictionaries

    # Serialize the list of dictionaries to JSON,
    # using the custom converter function to handle ObjectId
    serialized_persons = json.dumps(persons, default=convert_to_json)

    return JsonResponse(serialized_persons, safe=False)