from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CarForm
from .models import Car
from comments.forms import CommentForm
from comments.models import Comment

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'main_page/cars_list.html', {'cars': cars})

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()  # Получаем все комментарии для данного автомобиля

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

    return render(request, 'main_page/car_detail.html', {
        'car': car,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def car_add(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user  
            car.save()
            return redirect('cars_list')  
    else:
        form = CarForm()
    return render(request, 'main_page/car_add.html', {'form': form})

@login_required
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Проверяем, что текущий пользователь — владелец записи
    if car.owner != request.user:
        raise PermissionDenied("Вы не можете редактировать этот автомобиль.")

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cars_list') 
    else:
        form = CarForm(instance=car)

    return render(request, 'main_page/car_edit.html', {'form': form, 'car': car})


@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Проверяем, что текущий пользователь — владелец автомобиля
    if car.owner != request.user:
        raise PermissionDenied("Вы не можете удалить этот автомобиль.")

    # Убедитесь, что используется метод POST для удаления
    if request.method == 'POST':
        car.delete()
        return redirect('cars_list')  # Перенаправляем на список автомобилей после удаления

    # Если запрос не POST — показываем форму подтверждения
    return render(request, 'main_page/car_delete.html', {'car': car})
