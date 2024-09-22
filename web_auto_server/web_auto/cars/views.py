from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CarForm
from .models import Car
from comments.forms import CommentForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CarSerializer


class CarListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request): # GET /api/cars/ — получение списка автомобилей
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request): # POST /api/cars/ — создание нового автомобиля
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk): 
        try:
            return Car.objects.get(pk=pk)
        except Car.DoesNotExist:
            return None
        
    def get(self, request, pk): # GET /api/cars/<id>/ — получение информации о конкретном автомобиле
        car = self.get_object(pk)
        if car:
            serializer = CarSerializer(car)
            return Response(serializer.data)
        return Response({'detail': 'Car not found.'}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk): # PUT /api/cars/<id>/ — обновление информации о автомобиле
        car = self.get_object(pk)
        if car and car.owner == request.user:  
            serializer = CarSerializer(car, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'You do not have permission to edit this car.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk): # DELETE /api/cars/<id>/ — удаление автомобиля
        car = self.get_object(pk)
        if car and car.owner == request.user: 
            car.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'You do not have permission to delete this car.'}, status=status.HTTP_403_FORBIDDEN)

def cars_list(request): # список автомобилей
    cars = Car.objects.all()
    return render(request, 'cars/cars_list.html', {'cars': cars})

@login_required
def car_detail(request, car_id): # конкретный автомобиль
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all() 

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = car
            new_comment.user = request.user
            new_comment.save()
            return redirect('car_detail', car_id=car.id)
    else:
        comment_form = CommentForm()

    return render(request, 'cars/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def car_add(request): # добавление автомобиля
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  
            car.save()
            return redirect('cars_list')  
    else:
        form = CarForm()
    return render(request, 'cars/car_add.html', {'form': form})

@login_required
def car_edit(request, car_id): # изменение автомобиля
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        raise PermissionDenied("Вы не можете редактировать этот автомобиль.")

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cars_list') 
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_edit.html', {'form': form, 'car': car})


@login_required
def car_delete(request, car_id): # удаление автомобиля
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        raise PermissionDenied("Вы не можете удалить этот автомобиль.")

    if request.method == 'POST':
        car.delete()
        return redirect('cars_list') 

    return render(request, 'cars/car_delete.html', {'car': car})
