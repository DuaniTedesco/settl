import uuid
from django.db import models
from django.conf import settings


class Group(models.Model):
    TYPE_CHOICES = [
        ('republica', 'República'),
        ('coliving', 'Coliving'),
        ('familia', 'Família'),
        ('viagem', 'Viagem'),
        ('outro', 'Outro'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nome')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='republica', verbose_name='Tipo')
    description = models.TextField(blank=True, verbose_name='Descrição')
    invite_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='created_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_invite_link(self, request=None):
        path = f'/groups/join/{self.invite_token}/'
        if request:
            return request.build_absolute_uri(path)
        return path

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['-created_at']


class Membership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('member', 'Membro'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return f'{self.user.get_full_name()} em {self.group.name}'
