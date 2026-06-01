from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar_initials = models.CharField(max_length=2, blank=True)
    pix_key = models.CharField(max_length=100, blank=True, verbose_name='Chave Pix')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.avatar_initials:
            parts = self.get_full_name().strip().split()
            if len(parts) >= 2:
                self.avatar_initials = (parts[0][0] + parts[-1][0]).upper()
            elif parts:
                self.avatar_initials = parts[0][:2].upper()
            else:
                self.avatar_initials = self.email[:2].upper()
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
