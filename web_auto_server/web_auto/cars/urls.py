from django.urls import path
from . import views
from .views import CarListCreateView, CarDetailView

urlpatterns = [
    path('', views.cars_list, name='cars_list'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/', views.car_add, name='car_add'),
    path('cars/<int:car_id>/edit/', views.car_edit, name='car_edit'),
    path('cars/<int:car_id>/delete/', views.car_delete, name='car_delete'),
    
    #API methods
    path('api/cars/', CarListCreateView.as_view()),
    path("api/cars/<int:pk>/", CarDetailView.as_view()),

]
