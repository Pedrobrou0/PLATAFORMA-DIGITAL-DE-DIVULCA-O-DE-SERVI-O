# Plataforma Digital para Divulgação de Serviços Prestados por Profissionais Autônomos

Plataforma web desenvolvida em Python e Django para facilitar a conexão entre profissionais autônomos e clientes, permitindo a divulgação, busca, solicitação e avaliação de serviços.

O projeto está sendo desenvolvido como atividade acadêmica da disciplina de Programação de Sistemas Web (PSW).

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Arquitetura e modelagem](#arquitetura-e-modelagem)
- [Funcionalidades por aplicativo](#funcionalidades-por-aplicativo)
- [Principais rotas do projeto](#principais-rotas-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Como executar no Windows](#como-executar-no-windows)
- [Como executar no Linux](#como-executar-no-linux)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Banco de dados](#banco-de-dados)
- [Painel administrativo](#painel-administrativo)
- [Comandos úteis](#comandos-úteis)
- [Testes](#testes)
- [Solução de problemas comuns](#solução-de-problemas-comuns)
- [Boas práticas](#boas-práticas)
- [Fluxo de trabalho com Git](#fluxo-de-trabalho-com-git)
- [Documentação técnica](#documentação-técnica)
- [Equipe](#equipe)
- [Licença](#licença)
- [Status do projeto](#status-do-projeto)

## Sobre o projeto

A **Plataforma Digital para Divulgação de Serviços Prestados por Profissionais Autônomos** tem como objetivo facilitar a conexão entre profissionais e clientes.

A plataforma permitirá que visitantes consultem profissionais e serviços disponíveis, enquanto usuários cadastrados poderão utilizar funcionalidades que exigem identificação.

Entre as principais funcionalidades previstas estão:

- Cadastro e autenticação de clientes e profissionais.
- Gerenciamento do perfil dos profissionais.
- Cadastro e gerenciamento de serviços.
- Organização de profissionais e serviços por categorias.
- Busca de profissionais e serviços.
- Solicitação de serviços por clientes.
- Gerenciamento das solicitações pelos profissionais.
- Avaliações entre clientes e profissionais.
- Envio de feedbacks sobre a plataforma.
- Área de ajuda para clientes e profissionais.
- Administração da plataforma por meio do painel administrativo do Django.

O público-alvo do sistema são profissionais autônomos que prestam serviços (como manutenção, beleza, aulas particulares, consultoria, entre outros) e clientes que buscam contratar esses serviços de forma organizada, com histórico de solicitações e avaliações.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Git
- GitHub

## Estrutura do projeto

O projeto está organizado nos seguintes aplicativos Django:

- `usuarios`: funcionalidades relacionadas aos clientes e profissionais.
- `servicos`: funcionalidades relacionadas às categorias, serviços e solicitações.
- `interacoes`: funcionalidades relacionadas às solicitações de serviço entre clientes e profissionais.
- `suporte`: funcionalidades relacionadas aos feedbacks sobre a plataforma, avaliações e à área de ajuda.
- `config`: configurações gerais do projeto Django.

Estrutura básica:

```text
├── config/
├── interacoes/
├── servicos/
├── suporte/
├── usuarios/
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

Cada aplicativo segue a organização padrão do Django, com os arquivos:

```text
<app>/
├── migrations/
├── templates/<app>/
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

## Arquitetura e modelagem

O sistema utiliza herança de tabelas múltiplas (*multi-table inheritance*) do Django: o model `Profissional` estende o model padrão `User` do Django, reaproveitando a autenticação já pronta do framework (login, senha, permissões) e adicionando os campos específicos de um profissional autônomo (como categorias de atuação).

Os principais relacionamentos entre os models são:

- Um `Profissional` pode ter vários `Servico` cadastrados.
- Um `Servico` pertence a uma `Categoria`.
- Um `Servico` pode ter várias `Solicitacao` feitas por clientes.
- Uma `Solicitacao` possui um status (`StatusSolicitacao`), controlando o ciclo de vida do pedido: pendente, aceita, recusada, concluída ou cancelada.
- Um `Feedback` é enviado por um usuário sobre a plataforma, classificado por `TipoFeedback`.
- Uma `Avaliacao` é feita por um cliente ou por um profissional (`TipoAutorAvaliacao`) sobre a outra ponta da relação de serviço.

Todas as views do projeto são implementadas como **funções** (Function-Based Views), seguindo o padrão adotado pela equipe desde o início do desenvolvimento — o projeto não utiliza Class-Based Views.

## Funcionalidades por aplicativo

### `usuarios`

- Cadastro de profissionais (CRUD completo: criar, listar, detalhar, editar e excluir).
- Vínculo de um profissional a uma ou mais categorias de atuação.
- Exibição dos serviços vinculados a cada profissional em seu perfil.

### `servicos`

- CRUD completo de categorias (criar, listar, detalhar, editar e excluir).
- CRUD completo de serviços (criar, listar, detalhar, editar e excluir).
- Associação de cada serviço a um profissional e a uma categoria.

### `interacoes`

- CRUD completo de solicitações de serviço feitas por clientes.
- Modelo de dados já preparado para o ciclo de vida da solicitação (aceitar, recusar, cancelar e concluir), com os métodos correspondentes definidos em `Solicitacao`.

### `suporte`

- Modelos de `Feedback` (mensagens sobre a plataforma) e `Avaliacao` (avaliações entre cliente e profissional) já definidos e registrados no banco de dados.
- CRUD de tela (views, urls e templates) para feedback e avaliação em desenvolvimento pela equipe.

> As funcionalidades de busca por categoria, busca por palavra-chave, página inicial da plataforma e as ações de aceitar/recusar/cancelar solicitação estão descritas no Documento de Requisitos do projeto e em fase de implementação.

## Principais rotas do projeto

As rotas abaixo refletem as URLs já implementadas em cada aplicativo. Todas ficam disponíveis a partir da raiz configurada em `config/urls.py`.

**`usuarios`**

| Rota | Descrição |
|---|---|
| `/profissionais/` | Lista todos os profissionais cadastrados. |
| `/profissionais/novo/` | Formulário de cadastro de um novo profissional. |
| `/profissionais/<id>/` | Detalhe de um profissional específico. |
| `/profissionais/<id>/editar/` | Formulário de edição de um profissional. |
| `/profissionais/<id>/deletar/` | Confirmação e exclusão de um profissional. |

**`servicos`**

| Rota | Descrição |
|---|---|
| `/categorias/` | Lista todas as categorias cadastradas. |
| `/categorias/novo/` | Formulário de cadastro de uma nova categoria. |
| `/categorias/<id>/` | Detalhe de uma categoria específica. |
| `/categorias/<id>/editar/` | Formulário de edição de uma categoria. |
| `/categorias/<id>/deletar/` | Confirmação e exclusão de uma categoria. |
| `/servicos/` | Lista todos os serviços cadastrados. |
| `/servicos/novo/` | Formulário de cadastro de um novo serviço. |
| `/servicos/<id>/` | Detalhe de um serviço específico. |
| `/servicos/<id>/editar/` | Formulário de edição de um serviço. |
| `/servicos/<id>/deletar/` | Confirmação e exclusão de um serviço. |

**`interacoes`**

| Rota | Descrição |
|---|---|
| `/solicitacoes/` | Lista todas as solicitações cadastradas. |
| `/solicitacoes/novo/` | Formulário de criação de uma nova solicitação. |
| `/solicitacoes/<id>/` | Detalhe de uma solicitação específica. |
| `/solicitacoes/<id>/editar/` | Formulário de edição de uma solicitação. |
| `/solicitacoes/<id>/deletar/` | Confirmação e exclusão de uma solicitação. |

**`suporte`**

As rotas de feedback e avaliação estão em desenvolvimento e serão documentadas aqui assim que forem mescladas na branch principal.

## Pré-requisitos

Antes de executar o projeto, é necessário possuir:

- Python instalado.
- `pip`, gerenciador de pacotes do Python.
- Git.
- Suporte à criação de ambientes virtuais Python (`venv`).

O uso de um ambiente virtual é recomendado para manter as dependências do projeto isoladas das demais instalações Python da máquina.

## Como executar no Windows

### 1. Clone o repositório

```powershell
git clone URL_DO_REPOSITORIO
```

### 2. Acesse a pasta do projeto

```powershell
cd NOME_DO_REPOSITORIO
```

### 3. Crie o ambiente virtual

```powershell
py -m venv venv
```

### 4. Ative o ambiente virtual

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do script, execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente ativar novamente:

```powershell
.\venv\Scripts\Activate.ps1
```

No Prompt de Comando (CMD), utilize:

```cmd
venv\Scripts\activate.bat
```

### 5. Instale as dependências

```powershell
python -m pip install -r requirements.txt
```

### 6. Gere uma chave secreta para o ambiente local

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a chave exibida pelo terminal.

### 7. Crie o arquivo `.env`

Faça uma cópia do arquivo `.env.example`:

```cmd
copy .env.example .env
```

Abra o novo arquivo `.env` e substitua o valor de `SECRET_KEY` pela chave gerada anteriormente.

Exemplo:

```env
SECRET_KEY='SUA_CHAVE_GERADA'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 8. Execute as migrações

```powershell
python manage.py migrate
```

### 9. Inicie o servidor

```powershell
python manage.py runserver
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000/
```

## Como executar no Linux

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Acesse a pasta

```bash
cd NOME_DO_REPOSITORIO
```

### 3. Crie o ambiente virtual

```bash
python3 -m venv venv
```

### 4. Ative o ambiente virtual

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Gere uma chave secreta

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7. Crie o `.env`

```bash
cp .env.example .env
```

Abra o `.env` e informe a chave gerada:

```env
SECRET_KEY='SUA_CHAVE_GERADA'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 8. Execute as migrações

```bash
python manage.py migrate
```

### 9. Inicie o servidor

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Variáveis de ambiente

O projeto utiliza um arquivo `.env` para armazenar configurações locais e informações que não devem ser versionadas.

O repositório possui o arquivo:

```text
.env.example
```

Ele serve como modelo para a criação do `.env` de cada desenvolvedor.

As variáveis utilizadas inicialmente são:

```env
SECRET_KEY='SUA_CHAVE_GERADA'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave secreta usada pelo Django para assinar sessões, cookies e tokens. Nunca deve ser reaproveitada em produção nem commitada no repositório. |
| `DEBUG` | Ativa (`True`) ou desativa (`False`) o modo de depuração do Django. Deve ficar `False` em produção. |
| `ALLOWED_HOSTS` | Lista de hosts/domínios autorizados a servir a aplicação, separados por vírgula. |

O arquivo `.env` não deve ser enviado ao GitHub.

Cada integrante da equipe deve criar seu próprio `.env` após clonar o projeto.

## Banco de dados

Durante o desenvolvimento local, o projeto utiliza SQLite.

O arquivo:

```text
db.sqlite3
```

não é versionado no Git.

Cada desenvolvedor cria seu banco local executando:

```bash
python manage.py migrate
```

As migrations criadas pelos aplicativos Django devem ser versionadas normalmente.

Caso precise recomeçar o banco local do zero (por exemplo, depois de testar dados de exemplo), basta apagar o arquivo `db.sqlite3` e rodar `python manage.py migrate` novamente — isso não afeta o banco de outros integrantes da equipe, já que cada um mantém sua própria cópia local.

## Painel administrativo

O Django disponibiliza um painel administrativo em:

```text
http://127.0.0.1:8000/admin/
```

Para criar um superusuário local:

```bash
python manage.py createsuperuser
```

Depois de informar os dados solicitados, execute:

```bash
python manage.py runserver
```

e acesse `/admin/`.

Pelo painel administrativo é possível cadastrar, editar e remover diretamente os registros de qualquer model que esteja registrado em `admin.py`, o que é útil para popular dados de teste durante o desenvolvimento sem precisar passar pelas telas do site.

## Comandos úteis

Verificar a configuração do projeto:

```bash
python manage.py check
```

Criar migrations após alterações nos models:

```bash
python manage.py makemigrations
```

Aplicar migrations:

```bash
python manage.py migrate
```

Executar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Criar um superusuário:

```bash
python manage.py createsuperuser
```

Visualizar as dependências instaladas:

```bash
python -m pip freeze
```

Atualizar o arquivo de dependências:

```bash
python -m pip freeze > requirements.txt
```

Abrir o shell interativo do Django (útil para testar consultas rapidamente):

```bash
python manage.py shell
```

Desativar o ambiente virtual:

```bash
deactivate
```

## Testes

O projeto ainda não possui uma suíte de testes automatizados (os arquivos `tests.py` de cada aplicativo estão prontos para receber os testes, mas ainda vazios). Até que os testes automatizados sejam implementados, a equipe segue um checklist manual mínimo antes de qualquer commit que mexa em views, urls ou templates:

- [ ] O servidor sobe sem erros com `python manage.py runserver`.
- [ ] `python manage.py check` não aponta nenhum problema.
- [ ] As páginas alteradas carregam sem erro 500 no navegador.
- [ ] Os links de navegação (menu) continuam funcionando em todas as páginas.
- [ ] Formulários criados ou alterados salvam e validam corretamente (inclusive campos obrigatórios).
- [ ] As páginas de confirmação de exclusão realmente excluem o registro correto.
- [ ] Nenhuma migration pendente aparece em `python manage.py makemigrations --check`.

Quando os testes automatizados forem adicionados, a execução será feita com:

```bash
python manage.py test
```

## Solução de problemas comuns

**`ModuleNotFoundError: No module named 'django'`**
O ambiente virtual não está ativado, ou as dependências não foram instaladas. Ative o `venv` e rode novamente `pip install -r requirements.txt`.

**`django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty`**
O arquivo `.env` não foi criado ou está sem o valor de `SECRET_KEY`. Revise o passo de criação do `.env` descrito acima.

**`That port is already in use`**
Outro processo (às vezes um `runserver` anterior que não foi encerrado) já está usando a porta 8000. Finalize o processo anterior ou suba o servidor em outra porta:

```bash
python manage.py runserver 8001
```

**Erros ligados a migrations pendentes**
Depois de puxar alterações da equipe (`git pull`) que incluam mudanças em `models.py`, sempre rode:

```bash
python manage.py migrate
```

**`.venv` ou `venv` aparece no `git status`**
A pasta do ambiente virtual não deveria ser versionada. Confirme se `venv/` está listada no `.gitignore` antes de dar `git add`.

**Alterações que não aparecem no navegador**
Tente um refresh forçado da página (`Ctrl+F5`) e confirme que o servidor de desenvolvimento (`runserver`) foi reiniciado após a alteração, principalmente em arquivos Python (o autoreload nem sempre pega alterações em `urls.py`).

## Boas práticas

- Sempre utilizar um ambiente virtual durante o desenvolvimento.
- Não versionar a pasta `venv`.
- Não versionar o arquivo `.env`.
- Não versionar o banco local `db.sqlite3`.
- Versionar as migrations do Django.
- Manter o `requirements.txt` atualizado.
- Nunca armazenar senhas ou chaves secretas diretamente no código.
- Utilizar `.env.example` como referência para configuração do ambiente.
- Executar `python manage.py check` antes de commits importantes.
- Executar `python manage.py migrate` após receber novas migrations da equipe.
- Executar `git pull` antes de iniciar alterações quando houver mudanças remotas.
- Escrever mensagens de commit curtas e descritivas, no imperativo (ex.: "Adiciona filtro de serviços por categoria").
- Evitar commits que misturem funcionalidades diferentes sem relação entre si.
- Manter o padrão de Function-Based Views em todo o projeto, sem introduzir Class-Based Views.

## Fluxo de trabalho com Git

Para manter o histórico organizado, a equipe segue a sequência abaixo a cada alteração:

```bash
git pull origin main
```

Depois de implementar e testar a alteração localmente:

```bash
git add <arquivos alterados>
git commit -m "Mensagem descrevendo a alteração"
git push origin main
```

Recomendações:

- Sempre dar `git pull` antes de começar a mexer em qualquer arquivo, para evitar conflitos.
- Adicionar explicitamente os arquivos alterados (`git add <arquivo>`), evitando `git add .` quando não for necessário, para não versionar arquivos indesejados por engano.
- Um commit por alteração lógica, sempre que possível — facilita revisar o histórico depois.
- Resolver conflitos de merge localmente antes de dar `git push`.

## Documentação técnica

### Diagrama de Classes

O diagrama de classes apresenta as principais entidades do sistema, seus atributos, métodos e relacionamentos previstos para a aplicação.

![Diagrama de Classes](docs/diagramas/Classes_2.1.png)

### Diagrama de Casos de Uso

O Diagrama de Casos de Uso apresenta as principais funcionalidades da plataforma e as interações dos atores com o sistema, organizadas de acordo com os módulos funcionais definidos no Documento de Requisitos.

📄 [Visualizar documentação completa dos Casos de Uso](docs/documentos/Casos_de_Uso.pdf)

## Equipe

Projeto desenvolvido em trio para a disciplina de Programação de Sistemas Web (PSW):

- Pedro
- Davi
- Latrel

## Licença

Este é um projeto acadêmico, desenvolvido para fins educacionais no âmbito da disciplina de Programação de Sistemas Web (PSW). Não possui licença de uso comercial.

## Status do projeto

Projeto acadêmico em desenvolvimento.

A estrutura inicial do Django e a organização dos aplicativos estão configuradas. Os CRUDs de `usuarios`, `servicos` e `interacoes` já estão implementados. As funcionalidades e regras de negócio restantes — CRUD de tela do `suporte`, ações de aceitar/recusar/cancelar solicitação, busca por categoria e por palavra-chave, e página inicial — serão implementadas progressivamente durante o desenvolvimento.