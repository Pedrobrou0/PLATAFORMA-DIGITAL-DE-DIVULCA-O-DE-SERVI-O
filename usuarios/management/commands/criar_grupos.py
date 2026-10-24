from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

from usuarios.models import Profissional
from usuarios.permissoes import (
    GRUPO_PROFISSIONAL,
    PERMISSOES_POR_GRUPO,
)


class Command(BaseCommand):
    help = (
        'Cria (ou atualiza) os grupos Cliente, Profissional e '
        'Administrador com as permissões do django.contrib.auth.'
    )

    def handle(self, *args, **options):
        for nome_grupo, permissoes in PERMISSOES_POR_GRUPO.items():
            grupo, criado = Group.objects.get_or_create(
                name=nome_grupo
            )

            grupo.permissions.clear()

            for permissao in permissoes:
                app_label, codename = permissao.split('.')

                try:
                    objeto = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                except Permission.DoesNotExist:
                    raise CommandError(
                        f'Permissão {permissao} não encontrada. '
                        'Rode "python manage.py migrate" antes.'
                    )

                grupo.permissions.add(objeto)

            situacao = 'criado' if criado else 'atualizado'

            self.stdout.write(self.style.SUCCESS(
                f'Grupo {nome_grupo} {situacao} '
                f'com {len(permissoes)} permissões.'
            ))

        # Profissionais cadastrados antes da autenticação
        # entram no grupo Profissional.
        grupo_profissional = Group.objects.get(name=GRUPO_PROFISSIONAL)

        for profissional in Profissional.objects.all():
            profissional.groups.add(grupo_profissional)

        self.stdout.write(self.style.SUCCESS(
            'Profissionais já cadastrados adicionados ao grupo Profissional.'
        ))