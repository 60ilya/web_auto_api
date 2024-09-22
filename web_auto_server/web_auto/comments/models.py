from django.db import models
from django.contrib.auth.models import User
from main_page.models import Car

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.car}'
    