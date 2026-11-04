from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profissional


@admin.register(Profissional)
class ProfissionalAdmin(UserAdmin):
    # Reaproveita o admin de User do django.contrib.auth:
    # senha criptografada, grupos e permissões (Gerenciar Usuários).

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'cidade',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Dados do profissional', {
            'fields': ('telefone', 'cidade', 'descricao', 'foto'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados do profissional', {
            'fields': ('telefone', 'cidade', 'descricao'),
        }),
    )