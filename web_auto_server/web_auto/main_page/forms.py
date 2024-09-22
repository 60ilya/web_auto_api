from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
