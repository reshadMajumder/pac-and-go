from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,logout
from .models import CustomUser, Traveler, TourGuide
from .forms import TravelerRegistrationForm
from django.http import HttpResponse

from django .contrib.auth import authenticate,login,logout
from django .contrib.auth import login as auth_login


def register(request):
    if request.method == 'POST':
        # Debug: Print POST data
        print("POST data received:")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
            
        # Check if it's a traveler registration
        if request.POST.get('user_type') == 'traveler':
            # Check if passwords match first
            if request.POST.get('touristPassword') != request.POST.get('touristConfirmPassword'):
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
                
            # Create a new user with the traveler user type
            try:
                # Print debug information
                print(f"Creating user with email: {request.POST.get('touristEmail')}, user_type: traveler")
                
                # Check if email already exists
                if CustomUser.objects.filter(email=request.POST.get('touristEmail')).exists():
                    messages.error(request, "A user with that email already exists.")
                    return render(request, 'register.html')
                
                user = CustomUser.objects.create_user(
                    email=request.POST.get('touristEmail'),
                    password=request.POST.get('touristPassword'),
                    username=request.POST.get('touristEmail').split('@')[0],
                    first_name=request.POST.get('touristFirstName', ''),
                    last_name=request.POST.get('touristLastName', ''),
                    phone_number=request.POST.get('touristPhone', ''),
                    user_type='traveler'
                )
                
                # Print debug information
                print(f"User created: {user.email}, {user.username}")
                
                # Create the traveler profile
                traveler = Traveler.objects.create(user=user)
                print(f"Traveler profile created for user: {user.email}")
                
                # Log the user in
                login(request, user)
                messages.success(request, "Registration successful! Welcome to Pac-and-Go.")
                print("User logged in successfully")
                return redirect('/')  # Redirect to the root URL
            except Exception as e:
                # Print the error for debugging
                import traceback
                print(f"Registration error: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f"Registration failed: {str(e)}")
        elif request.POST.get('user_type') == 'tour_guide':
            # Check if passwords match first
            if request.POST.get('guidePassword') != request.POST.get('guideConfirmPassword'):
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
                
            try:
                # Print debug information
                print(f"Creating tour guide with email: {request.POST.get('guideEmail')}, user_type: tour_guide")
                
                # Check if email already exists
                if CustomUser.objects.filter(email=request.POST.get('guideEmail')).exists():
                    messages.error(request, "A user with that email already exists.")
                    return render(request, 'register.html')
                
                # Create a new user with the tour guide user type
                user = CustomUser.objects.create_user(
                    email=request.POST.get('guideEmail'),
                    password=request.POST.get('guidePassword'),
                    username=request.POST.get('guideEmail').split('@')[0],
                    first_name=request.POST.get('guideFirstName', ''),
                    last_name=request.POST.get('guideLastName', ''),
                    phone_number=request.POST.get('guidePhone', ''),
                    user_type='tour_guide'
                )
                
                # Print debug information
                print(f"Tour guide user created: {user.email}, {user.username}")
                
                # Convert experience to int with default if there's a problem
                try:
                    experience_years = int(request.POST.get('guideExperience', 0))
                except (ValueError, TypeError):
                    experience_years = 0
                    print(f"Warning: Could not convert guideExperience '{request.POST.get('guideExperience')}' to int, using 0")
                
                # Create the tour guide profile
                tour_guide = TourGuide.objects.create(
                    user=user,
                    location=request.POST.get('guideLocation', ''),
                    experience_years=experience_years,
                    bio=request.POST.get('guideBio', '')
                )
                print(f"Tour guide profile created for user: {user.email}")
                
                # Log the user in
                login(request, user)
                messages.success(request, "Registration successful! Welcome to Pac-and-Go.")
                print("Tour guide logged in successfully")
                return redirect('/')  # Redirect to the root URL
            except Exception as e:
                # Print the error for debugging
                import traceback
                print(f"Guide registration error: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Invalid user type selected.")
            print(f"Invalid user type: {request.POST.get('user_type')}")
    
    # For GET requests, just render the template
    return render(request, 'register.html')




def  handle_login(request):
    if request.method ==  "POST":
        data=request.POST

        username=data.get('email')
        password=data.get('password')


        user=authenticate(username=username,password=password)
        if user is not None:
            auth_login(request,user)
            print("logged in")
           
            return redirect('home')
        
        
        
        else:
            messages.error(request,'Username or Password is incorrect')
            print("not in")

            return redirect('login')
    return render ( request, 'login.html')


def handlelogout(request):
    logout(request)
    return redirect('home')