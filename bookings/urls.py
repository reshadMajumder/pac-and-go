from django.urls import path
from .views import home,package_details,contact_us,about_us

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_us, name='about'),
    path('contact/', contact_us, name='contact'),
    path('package-details/<int:id>', package_details, name='package-details'),

]
