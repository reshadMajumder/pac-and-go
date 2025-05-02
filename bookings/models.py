from django.db import models

# Create your models here.
class TourLocation(models.Model):
    location=models.CharField(max_length=100,null=True,blank=True)
    hotel=models.CharField(max_length=100,null=True,blank=True)


class PackageHighlights(models.Model):
    highlight=models.CharField(max_length=100,null=True,blank=True)




class Packages(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='packageImage/')
    location=models.ManyToManyField(TourLocation, related_name='tourlocation')
    highlight=models.ManyToManyField(PackageHighlights,related_name='packagehighlights')
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    details=models.TextField()
    complementary=models.CharField(max_length=20,null=True,blank=True ,choices=[('breakfast', 'Breakfast'), ('all_meals', 'All Meals'),('breakfast_lunch','Breakfast & Lunch')])

    
