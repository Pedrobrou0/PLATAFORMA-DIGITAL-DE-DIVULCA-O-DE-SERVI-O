#!/usr/bin/env bash
# Comandos que o Render roda a cada deploy (Build Command: bash build.sh).
# Se qualquer comando falhar, o deploy para (set -o errexit).
set -o errexit

# Instala o Django e os pacotes do requirements.txt
pip install -r requirements.txt

# Junta o CSS e o JS do AdminLTE na pasta staticfiles/ (WhiteNoise entrega)
python manage.py collectstatic --no-input

# Cria e atualiza as tabelas no Postgres
python manage.py migrate

# Cria os grupos Cliente, Profissional e Administrador com as permissões
python manage.py criar_grupos

# Cria o superusuário com as variáveis DJANGO_SUPERUSER_* do Render.
# O "|| true" evita erro quando ele já existe (nos deploys seguintes).
python manage.py createsuperuser --no-input || true
