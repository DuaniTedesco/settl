from django.db import models
from django.conf import settings
from decimal import Decimal


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('aluguel', 'Aluguel'),
        ('agua', 'Água'),
        ('energia', 'Energia elétrica'),
        ('internet', 'Internet'),
        ('gas', 'Gás'),
        ('alimentacao', 'Alimentação'),
        ('limpeza', 'Limpeza'),
        ('manutencao', 'Manutenção'),
        ('transporte', 'Transporte'),
        ('lazer', 'Lazer'),
        ('outro', 'Outro'),
    ]

    SPLIT_TYPE_CHOICES = [
        ('equal', 'Igualitária'),
        ('custom', 'Personalizada'),
        ('percentage', 'Por percentual'),
    ]

    RECURRENCE_CHOICES = [
        ('none', 'Sem recorrência'),
        ('monthly', 'Mensal'),
        ('weekly', 'Semanal'),
        ('biweekly', 'Quinzenal'),
    ]

    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200, verbose_name='Descrição')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor (R$)')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='outro')
    paid_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='paid_expenses', verbose_name='Pago por'
    )
    split_type = models.CharField(max_length=15, choices=SPLIT_TYPE_CHOICES, default='equal')
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    date = models.DateField(verbose_name='Data')
    notes = models.TextField(blank=True, verbose_name='Observações')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_expenses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description} — R$ {self.amount}'

    def save_equal_shares(self, members):
        self.shares.all().delete()
        n = len(members)
        if n == 0:
            return
        base = (self.amount / n).quantize(Decimal('0.01'))
        remainder = self.amount - base * n
        for i, user in enumerate(members):
            extra = remainder if i == 0 else Decimal('0.00')
            ExpenseShare.objects.create(expense=self, user=user, amount=base + extra)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-date', '-created_at']


class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expense_shares')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('expense', 'user')

    def __str__(self):
        return f'{self.user.get_full_name()} deve R$ {self.amount} em {self.expense.description}'


class Settlement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Aguardando confirmação'),
        ('confirmed', 'Confirmado'),
        ('disputed', 'Disputado'),
    ]

    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='settlements')
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='settlements_made', verbose_name='Quem pagou'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='settlements_received', verbose_name='Quem recebeu'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pix_key_used = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Acerto'
        verbose_name_plural = 'Acertos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.payer.get_full_name()} → {self.receiver.get_full_name()} R$ {self.amount}'
