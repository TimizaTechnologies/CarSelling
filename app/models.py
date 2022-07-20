from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
from django.utils.html import mark_safe

class Car(models.Model):
    state_choice=(
        ('US', 'USA'),
        ('IN', 'India'),
        ('NZ', 'New Zealand'),
        ('CN', 'China'),
        ('CL', 'Chile'),
    )
    year_choice= []
    for r in range(2000, (datetime.now().year+1)):
        year_choice.append((r,r))

    features_choices = (
        ('Cruise Control', 'Cruise Control'),
        ('Audio Interface', 'Audio Interface'),
        ('Airbags', 'Airbags'),
        ('Air Conditioning', 'Air Conditioning'),
        ('Seat Heating', 'Seat Heating'),
        ('Alarm System', 'Alarm System'),
        ('ParkAssist', 'ParkAssist'),
        ('Power Steering', 'Power Steering'),
        ('Reversing Camera', 'Reversing Camera'),
        ('Direct Fuel Injection', 'Direct Fuel Injection'),
        ('Auto Start/Stop', 'Auto Start/Stop'),
        ('Wind Deflector', 'Wind Deflector'),
        ('Bluetooth Handset', 'Bluetooth Handset'),
    )

    door_choices = (
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )

    car_title=models.CharField(max_length=255)
    state=models.CharField(choices=state_choice, max_length=100)
    city=models.CharField(max_length=100)
    color=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.IntegerField(('year'), choices=year_choice)
    condition=models.CharField(max_length=100)
    price=models.IntegerField()
    description=RichTextField()
    car_photo=models.ImageField(upload_to='photos/%Y/%m/%d/')
    car_photo1=models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo2=models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo3=models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    car_photo4=models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    features=MultiSelectField(choices=features_choices)
    body_style=models.CharField(max_length=100)
    engine=models.CharField(max_length=100)
    transmission=models.CharField(max_length=100)
    interior=models.CharField(max_length=100)
    miles=models.IntegerField()
    doors=models.CharField(choices=door_choices, max_length=10)
    passengers=models.IntegerField()
    vin_no=models.CharField(max_length=100)
    milage=models.IntegerField()
    fuel_type=models.CharField(max_length=50)
    no_of_owners=models.CharField(max_length=100)
    is_featured=models.BooleanField(default=False)
    created_date=models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.car_title

    @property
    def thumbnail_preview(self):
        if self.car_photo:
            return mark_safe('<img src="{}" width="40" height="40" />'.format(self.car_photo.url))
        return ""


class Contact(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    car_id=models.IntegerField()
    customer_need=models.CharField(max_length=100)
    car_title=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    message=models.TextField(blank=True)
    user_id=models.IntegerField(blank=True)
    create_date=models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return self.email


class Team(models.Model):
    first_name= models.CharField(max_length=300, blank=False)
    last_name= models.CharField(max_length=255, blank=False)
    designation= models.CharField(max_length=255, blank=False)
    photo= models.ImageField(upload_to='photos/%Y/%m/%d/', blank=False)
    facebook_link= models.URLField(max_length=255)
    twitter_link= models.URLField(max_length=255)
    google_plus_link= models.URLField(max_length=255)
    created_date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name