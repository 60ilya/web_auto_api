from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path('cars/<int:car_id>/comments/', CommentListCreateView.as_view(), name='comment_list_create'),
]