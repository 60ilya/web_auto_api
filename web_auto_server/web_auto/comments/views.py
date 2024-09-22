from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

    def get_queryset(self):
        car_id = self.kwargs['car_id']
        return Comment.objects.filter(car_id=car_id)

    def perform_create(self, serializer):
        car_id = self.kwargs['car_id']
        serializer.save(user=self.request.user, car_id=car_id)