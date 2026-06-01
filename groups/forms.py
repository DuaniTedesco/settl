from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'type', 'description')
        labels = {
            'name': 'Nome da república/grupo',
            'type': 'Tipo',
            'description': 'Descrição',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
