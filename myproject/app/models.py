from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    
class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

class TestDrive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
class ECar(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    photo = models.ImageField(upload_to='car/', null=True)
    
    # New fields
    battery_capacity = models.FloatField(help_text="Battery capacity in kWh")
    range = models.FloatField(help_text="Range in miles")
    horsepower = models.IntegerField(help_text="Horsepower in HP")
    transmission = models.CharField(max_length=50, help_text="Transmission type")
    dimensions = models.CharField(max_length=100, help_text="Dimensions (e.g., LxWxH in inches)")
    weight = models.FloatField(help_text="Weight in lbs")
    seating_capacity = models.IntegerField(help_text="Seating capacity in seats")
    drive_type = models.CharField(max_length=50, help_text="Drive type (e.g., AWD, FWD, RWD)")

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


        return f"{self.year} {self.make} {self.model} {self.photo}"

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.username}\'s Wallet - Balance: ${self.balance}'

    def add_funds(self, amount):
        if amount <= 0:
            raise ValidationError('Amount must be positive.')
        self.balance += amount
        self.save()

    def deduct_funds(self, amount):
        if amount <= 0:
            raise ValidationError('Amount must be positive.')
        if self.balance < amount:
            raise ValidationError('Insufficient funds.')
        self.balance -= amount
        self.save()
class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction: ${self.amount} - {self.description}'        
from django.db import models

class NCar(models.Model):
    CAR_TYPE_CHOICES = [
        ('economy', 'Economy'),
        ('compact', 'Compact'),
        ('massive', 'Massive'),
        ('suv', 'SUV'),
        ('standard', 'Standard'),
    ]
    
    PASSENGER_CHOICES = [
        ('1-2', '1-2 Passengers'),
        ('3-5', '3-5 Passengers'),
        ('6_or_more', '6 or More Passengers'),
    ]
    
    BAG_CHOICES = [
        ('1-2', '1-2 Bags'),
        ('3-5', '3-5 Bags'),
        ('6_or_more', '6 or More Bags'),
    ]

    city = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    passengers = models.CharField(max_length=20, choices=PASSENGER_CHOICES)
    bags = models.CharField(max_length=20, choices=BAG_CHOICES)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    # Other relevant fields

    def __str__(self):
        return f"{self.city} - {self.car_type} ({self.passengers} passengers, {self.bags} bags)"
