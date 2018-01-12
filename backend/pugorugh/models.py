from django.contrib.auth.models import User
from django.db import models
from multiselectfield import MultiSelectField

MALE = 'm'
FEMALE = 'f'
UNKNOWN = 'u'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (UNKNOWN, 'Unknown'),
)

SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
EXTRA_LARGE = 'xl'
SIZE_CHOICES = (
    (SMALL, 'Small'),
    (MEDIUM, 'Medium'),
    (LARGE, 'Large'),
    (EXTRA_LARGE, 'Extra Large'),
    (UNKNOWN, 'Unknown'),
)

LIKED = 'l'
DISLIKED = 'd'
STATUS_CHOICES = (
    (LIKED, 'Like'),
    (DISLIKED, 'Dislike'),
)

BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'
AGE_CHOICES = (
    (BABY, 'Baby'),
    (YOUNG, 'Young'),
    (ADULT, 'Adult'),
    (SENIOR, 'Senior'),
)

class Dog(models.Model):
    name = models.CharField(max_length=20)
    image_filename = models.CharField(max_length=200)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=UNKNOWN
    )
    size = models.CharField(
        max_length=1,
        choices=SIZE_CHOICES,
        default=UNKNOWN
    )
    
    
class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, 
        choices=STATUS_CHOICES,
        default=LIKED
    )
    
class UserPref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = MultiSelectField(
        choices=AGE_CHOICES,
        #default=BABY
    )
    gender = MultiSelectField(
        choices=GENDER_CHOICES,
        #default=MALE
    )
    size = MultiSelectField(
        choices=SIZE_CHOICES,
        #default=SMALL
    )