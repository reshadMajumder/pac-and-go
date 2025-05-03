from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import datetime
from .models import Packages, TourLocation, PackageHighlights
from payments.models import Booking

# Create your views here.


def home(request):
    packages = Packages.objects.all()
    
    
    return render(request, 'index.html', context={"packages": packages})




def package_details(request, package_id):
    package = get_object_or_404(Packages, id=package_id)
    return render(request, 'package-details.html', {'package': package})

def about_us(request):
    return render(request,'about.html')

def contact_us(request):
    return render(request,'contact.html')


@login_required
def dashboard(request):
    # Common context for all users
    context = {
        "today": datetime.today(),
    }
    
    # Check user type and prepare specific context
    if hasattr(request.user, 'user_type'):
        if request.user.user_type == 'tour_guide':
            # Get tour guide profile
            try:
                tour_guide = request.user.guide_profile
                
                # Tour guide specific context
                packages = Packages.objects.filter(tour_guide=tour_guide)
                
                # Get bookings for all packages created by this guide
                bookings = Booking.objects.filter(package__in=packages).select_related('user', 'package', 'package__tour_guide', 'package__tour_guide__user')
                
                # Get user's own bookings (as traveler)
                traveler_bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__tour_guide', 'package__tour_guide__user')
                
                recent_activities = []
                
                context.update({
                    "packages": packages,
                    "bookings": bookings,
                    "traveler_bookings": traveler_bookings,
                    "recent_activities": recent_activities,
                    "guide_profile": tour_guide,
                })
            except:
                # Handle case where guide profile doesn't exist
                context.update({
                    "packages": [],
                    "bookings": [],
                    "traveler_bookings": [],
                    "recent_activities": [],
                    "guide_profile": None,
                    "profile_error": "Please complete your tour guide profile.",
                })
        else:
            # Traveler specific context
            traveler_bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__tour_guide', 'package__tour_guide__user')
            saved_packages = []  # In the future, you can add: SavedPackage.objects.filter(traveler__user=request.user)
            upcoming_trips = traveler_bookings.filter(status='Success').count()  # Count of upcoming bookings
            featured_packages = Packages.objects.all().order_by('-created_at')[:6]  # Get some featured packages
            
            context.update({
                "traveler_bookings": traveler_bookings,
                "saved_packages": saved_packages,
                "upcoming_trips": upcoming_trips,
                "featured_packages": featured_packages,
                "traveler_profile": request.user.traveler_profile if hasattr(request.user, 'traveler_profile') else None,
            })
    
    return render(request, 'dashboard.html', context)

@login_required
def create_package(request):
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile associated with the user
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            location_str = request.POST.get('location')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            details = request.POST.get('details')
            complementary = request.POST.get('complementary')
            
            # Create the package without many-to-many fields first
            package = Packages.objects.create(
                title=title,
                main_location=location_str,
                price=price,
                image=image,
                start_date=start_date,
                end_date=end_date,
                details=details,
                complementary=complementary,
                tour_guide=tour_guide
            )
            
            # Handle tour locations
            tour_locations = request.POST.getlist('tour_location[]')
            tour_hotels = request.POST.getlist('tour_hotel[]')
            
            for i in range(len(tour_locations)):
                if tour_locations[i] and i < len(tour_hotels):
                    location = TourLocation.objects.create(
                        location=tour_locations[i],
                        hotel=tour_hotels[i]
                    )
                    package.location.add(location)  # Adding to many-to-many field
            
            # Handle package highlights
            highlights = request.POST.getlist('highlight[]')
            for highlight_text in highlights:
                if highlight_text:
                    highlight = PackageHighlights.objects.create(highlight=highlight_text)
                    package.highlight.add(highlight)  # Adding to many-to-many field
            
            messages.success(request, 'Package created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating package: {str(e)}')
        
        return redirect('dashboard')
    
    # If not POST, redirect to the dashboard
    return redirect('dashboard')

@login_required
def delete_package(request, package_id):
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    package = get_object_or_404(Packages, id=package_id)
    
    # Check if the package belongs to the logged-in guide
    if package.tour_guide.user != request.user:
        return HttpResponseForbidden("You cannot delete a package that doesn't belong to you.")
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully!')
    
    return redirect('dashboard')

@login_required
def update_package(request, package_id):
    # Check if the user is a tour guide
    if not hasattr(request.user, 'user_type') or request.user.user_type != 'tour_guide':
        return HttpResponseForbidden("Access denied. You must be a tour guide to access this page.")
    
    # Get the tour guide profile
    try:
        tour_guide = request.user.guide_profile
    except:
        return HttpResponseForbidden("You need to complete your tour guide profile first.")
    
    package = get_object_or_404(Packages, id=package_id)
    
    # Check if the package belongs to the logged-in guide
    if package.tour_guide.user != request.user:
        return HttpResponseForbidden("You cannot update a package that doesn't belong to you.")
    
    if request.method == 'POST':
        try:
            # Get form data
            package.title = request.POST.get('title')
            package.main_location = request.POST.get('location')
            package.price = request.POST.get('price')
            if 'image' in request.FILES:
                package.image = request.FILES.get('image')
            package.start_date = request.POST.get('start_date')
            package.end_date = request.POST.get('end_date')
            package.details = request.POST.get('details')
            package.complementary = request.POST.get('complementary')
            
            package.save()
            
            # Handle tour locations (clear existing and add new)
            package.location.clear()
            tour_locations = request.POST.getlist('tour_location[]')
            tour_hotels = request.POST.getlist('tour_hotel[]')
            
            for i in range(len(tour_locations)):
                if tour_locations[i] and i < len(tour_hotels):
                    location = TourLocation.objects.create(
                        location=tour_locations[i],
                        hotel=tour_hotels[i]
                    )
                    package.location.add(location)
            
            # Handle package highlights (clear existing and add new)
            package.highlight.clear()
            highlights = request.POST.getlist('highlight[]')
            for highlight_text in highlights:
                if highlight_text:
                    highlight = PackageHighlights.objects.create(highlight=highlight_text)
                    package.highlight.add(highlight)
            
            messages.success(request, 'Package updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating package: {str(e)}')
        
        return redirect('dashboard')
    
    # If not POST, redirect to the dashboard
    return redirect('dashboard')

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Update user information
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.phone_number = request.POST.get('phone_number')
        request.user.address = request.POST.get('address')
        request.user.save()
        
        # Update type-specific profile
        if hasattr(request.user, 'user_type'):
            if request.user.user_type == 'tour_guide' and hasattr(request.user, 'guide_profile'):
                # Update guide profile
                guide_profile = request.user.guide_profile
                guide_profile.location = request.POST.get('location')
                guide_profile.experience_years = request.POST.get('experience_years')
                guide_profile.languages = request.POST.get('languages')
                guide_profile.expertise = request.POST.get('expertise')
                guide_profile.bio = request.POST.get('bio')
                guide_profile.save()
            elif request.user.user_type == 'traveler' and hasattr(request.user, 'traveler_profile'):
                # Update traveler profile
                traveler_profile = request.user.traveler_profile
                traveler_profile.preferences = request.POST.get('preferences')
                traveler_profile.interests = request.POST.get('interests')
                traveler_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
    
    return redirect('dashboard')

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        request.user.profile_picture = request.FILES.get('profile_picture')
        request.user.save()
        messages.success(request, 'Profile picture updated successfully!')
    
    return redirect('dashboard')

@login_required
def order_details(request, booking_id):
    """View to display detailed information about a specific booking."""
    # Get the booking and check permissions
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: only the traveler who booked or the tour guide of the package can view
    is_owner = booking.user == request.user
    is_guide = False
    
    # Check if the user is a tour guide and has access to this booking
    if hasattr(request.user, 'user_type') and request.user.user_type == 'tour_guide':
        try:
            tour_guide = request.user.guide_profile
            if booking.package.tour_guide == tour_guide:
                is_guide = True
        except:
            pass
    
    if not (is_owner or is_guide):
        return HttpResponseForbidden("You don't have permission to view this booking.")
    
    context = {
        'booking': booking,
        'is_owner': is_owner,
        'is_guide': is_guide,
    }
    
    return render(request, 'order_details.html', context)