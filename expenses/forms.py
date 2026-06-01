from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Expense, Settlement

User = get_user_model()


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('description', 'amount', 'category', 'paid_by', 'split_type', 'recurrence', 'date', 'notes')
        labels = {
            'description': 'Descrição',
            'amount': 'Valor (R$)',
            'category': 'Categoria',
            'paid_by': 'Pago por',
            'split_type': 'Divisão',
            'recurrence': 'Recorrência',
            'date': 'Data',
            'notes': 'Observações',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members = group.memberships.filter(is_active=True).select_related('user')
        users = [m.user for m in members]
        self.fields['paid_by'].queryset = User.objects.filter(
            pk__in=[u.pk for u in users]
        )
        self.fields['paid_by'].label_from_instance = lambda u: u.get_full_name()
        if not self.initial.get('date'):
            self.initial['date'] = timezone.now().date()


class SettlementForm(forms.ModelForm):
    class Meta:
        model = Settlement
        fields = ('receiver', 'amount', 'pix_key_used', 'notes')
        labels = {
            'receiver': 'Pagar para',
            'amount': 'Valor (R$)',
            'pix_key_used': 'Chave Pix usada',
            'notes': 'Observações',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, group, payer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members = group.memberships.filter(is_active=True).select_related('user')
        users = [m.user for m in members if m.user != payer]
        self.fields['receiver'].queryset = User.objects.filter(pk__in=[u.pk for u in users])
        self.fields['receiver'].label_from_instance = lambda u: u.get_full_name()
