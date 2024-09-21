from django.shortcuts import render
from .models import Car

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'main_page/cars_list.html', {'cars': cars})

# def car_info(request):
#     return render(request, 'main_page/car_info.html')

