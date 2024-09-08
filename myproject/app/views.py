from django.contrib import  messages,auth
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car,ECar,TestDrive,Wallet,Transaction,NCar
from .forms import TestDriveForm, CarSearchForm,CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger(__name__)
 
def add_funds(request):
    return render(request, 'add_funds.html', {
        'STRIPE_TEST_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY
    })

@csrf_exempt
def create_charge(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        amount = float(data.get('amount'))

        if not token or amount <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid token or amount'})

        try:
            # Create a charge with Stripe
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Convert dollars to cents
                currency='usd',
                source=token,
                description='Add funds to wallet',
            )

            # Add funds to the wallet
            wallet = Wallet.objects.get(user=request.user)
            wallet.add_funds(amount, 'Added funds via Stripe')

            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            return JsonResponse({'success': False, 'error': str(e)})
        except Wallet.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Wallet not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred: ' + str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
def Transaction(request):
    return render(request, 'transaction.html')

#     try:
#         wallet = Wallet.objects.get(user=request.user)
#         transactions = Transaction.objects.filter(wallet=wallet).order_by('-created_at')
#     except Wallet.DoesNotExist:
#         transactions = []

#     return render(request, 'transaction.html', {
#         'transactions': transactions
#     })
def wallet(request):
    cars = ECar.objects.all
    return render(request, 'wallet.html', { 'cars': cars})
 

     
# def car(request):
#     cars = EvCar.objects.all()
#     return render(request, 'car.html', {'cars': cars})

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to a home page or other after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


    




def logout(request):
    auth.logout(request)
    return redirect('/')

def book(request):
    if request.method == 'GET':
        car_ids = request.GET.getlist('cars')  # Retrieve selected car IDs from query parameters
        cars_to_compare = EvCar.objects.filter(id__in=car_ids)
        
        # Example: Calculate average price
        total_price = sum(car.price for car in cars_to_compare)
        average_price = total_price / len(cars_to_compare) if cars_to_compare else 0

        context = {
            'cars_to_compare': cars_to_compare,
            'average_price': average_price,
        }
        return render(request, 'profile.html', context)
    
    else:
        # Handle other HTTP methods if needed
        return HttpResponseNotAllowed(['GET'])

def compare_cars(request):
    if request.method == 'POST':
        car_ids = request.POST.getlist('compare_car')
        cars_to_compare = ECar.objects.filter(id__in=car_ids)
        # Perform comparison logic here (e.g., calculate differences, similarities)
        context = {
            'cars_to_compare': cars_to_compare,
        }
        return render(request, 'profile.html', context)

    cars = ECar.objects.all()
    context = {
        'cars': cars,
    }
    return render(request, 'compare_cars.html', context)  

def brand(request):
    brands = ECar.objects.values_list('make', flat=True).distinct()
    return render(request, 'brand.html', {'brands': brands})

def car_list(request, make):
    cars = ECar.objects.filter(make=make)
    return render(request, 'car_list.html', {'make': make, 'cars': cars})

def car(request, car_id):
    car = get_object_or_404(ECar, id=car_id)
    return render(request, 'car.html', {'car': car })

def car_search(request):
    form = CarSearchForm(request.GET or None)

    # Start with all cars
    cars = ECar.objects.all()

    # If form is submitted and valid, apply filters
    if form.is_valid():
        # Extract cleaned data from form
        cleaned_data = form.cleaned_data
        make = cleaned_data.get('make')
        model = cleaned_data.get('model')
        year_min = cleaned_data.get('year_min')
        year_max = cleaned_data.get('year_max')
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')
        battery_capacity_min = cleaned_data.get('battery_capacity_min')
        battery_capacity_max = cleaned_data.get('battery_capacity_max')
        range_min = cleaned_data.get('range_min')
        range_max = cleaned_data.get('range_max')
        horsepower_min = cleaned_data.get('horsepower_min')
        horsepower_max = cleaned_data.get('horsepower_max')
        transmission = cleaned_data.get('transmission')
        dimensions = cleaned_data.get('dimensions')
        weight_min = cleaned_data.get('weight_min')
        weight_max = cleaned_data.get('weight_max')
        seating_capacity = cleaned_data.get('seating_capacity')
        drive_type = cleaned_data.get('drive_type')

        # Apply filters based on cleaned data
        if make:
            cars = cars.filter(make__icontains=make)
        if model:
            cars = cars.filter(model__icontains=model)
        if year_min:
            cars = cars.filter(year__gte=year_min)
        if year_max:
            cars = cars.filter(year__lte=year_max)
        if price_min:
            cars = cars.filter(price__gte=price_min)
        if price_max:
            cars = cars.filter(price__lte=price_max)
        if battery_capacity_min:
            cars = cars.filter(battery_capacity__gte=battery_capacity_min)
        if battery_capacity_max:
            cars = cars.filter(battery_capacity__lte=battery_capacity_max)
        if range_min:
            cars = cars.filter(range__gte=range_min)
        if range_max:
            cars = cars.filter(range__lte=range_max)
        if horsepower_min:
            cars = cars.filter(horsepower__gte=horsepower_min)
        if horsepower_max:
            cars = cars.filter(horsepower__lte=horsepower_max)
        if transmission:
            cars = cars.filter(transmission__icontains=transmission)
        if dimensions:
            cars = cars.filter(dimensions__icontains=dimensions)
        if weight_min:
            cars = cars.filter(weight__gte=weight_min)
        if weight_max:
            cars = cars.filter(weight__lte=weight_max)
        if seating_capacity:
            cars = cars.filter(seating_capacity=seating_capacity)
        if drive_type:
            cars = cars.filter(drive_type__icontains=drive_type)

    return render(request, 'car_search.html', {
        'form': form,
        'cars': cars,
    })
    # query = request.GET.get('query', " ")
    # if query:
    #     cars = ECar.objects.filter(
    #         make__icontains=query
    #     ) | ECar.objects.filter(
    #         model__icontains=query
    #     )
    # else:
    #     cars = ECar.objects.all()
     

    # return render(request, 'car_search.html', {'cars': cars, 'query': query })

    # if form.is_valid():
    #     if form.cleaned_data.get('make'):
    #         cars = cars.filter(make__icontains=form.cleaned_data['make'])
    #     if form.cleaned_data.get('model'):
    #         cars = cars.filter(model__icontains=form.cleaned_data['model'])
    #     if form.cleaned_data.get('year_min'):
    #         cars = cars.filter(year__gte=form.cleaned_data['year_min'])
    #     if form.cleaned_data.get('year_max'):
    #         cars = cars.filter(year__lte=form.cleaned_data['year_max'])
    #     if form.cleaned_data.get('price_min'):
    #         cars = cars.filter(price__gte=form.cleaned_data['price_min'])
    #     if form.cleaned_data.get('price_max'):
    #         cars = cars.filter(price__lte=form.cleaned_data['price_max'])

    # return render(request, 'car_search.html', {'form': form, 'cars': cars})
def profile(request):
    return render (request, 'profile.html')

def about(request):
    return render(request, 'about.html')

