from django.db import models
from django.contrib.auth.models import User 

class Car(models.Model):
    make = models.CharField(max_length=50)  # Марка автомобиля
    model = models.CharField(max_length=50)  # Модель автомобиля
    year = models.PositiveIntegerField()  # Год выпуска
    description = models.TextField(null=True, blank=True)  # Описание автомобиля
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец автомобиля
    
    class Meta:
        permissions = [
            ("edit_car", "Can edit car"),
        ]

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
    