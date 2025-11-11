# SIGMA - Sistema Integrado de Gestão e Monitoramento Acadêmico

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-black?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy)

</div>

**SIGMA** é um sistema de gerenciamento acadêmico completo, desenvolvido em Flask. Ele foi projetado para conectar Alunos, Professores e a Diretoria, centralizando o gerenciamento de notas, frequência, atividades e usuários em uma plataforma única.

## Funcionalidades Principais

O sistema é dividido em três perfis de usuário principais, cada um com seu próprio dashboard e permissões.

### Portal do Aluno
* **Login por RA** (Registro Acadêmico).
* **Dashboard principal** com a lista de matérias em que está inscrito.
* **Visualização de Matéria:**
    * Lista de todas as atividades (passadas e futuras).
    * Consulta de notas obtidas em cada atividade.
    * Histórico detalhado de presença (frequência).
* **Entrega de Atividades:**
    * Página dedicada para responder e enviar atividades.
    * Bloqueio de reenvio após a primeira entrega.

### Portal do Professor
* **Login por Email** institucional.
* **Dashboard principal** com as matérias que leciona.
* **Gerenciamento de Matéria:**
    * Lista de todos os alunos inscritos.
    * Criação de novas atividades com título, descrição e data de entrega.
* **Lançamento de Presença:**
    * Sistema para registrar a frequência (presente/ausente) dos alunos em uma data específica.
* **Correção de Atividades:**
    * Visualização de todas as entregas feitas pelos alunos para uma atividade.
    * Atribuição de notas (0 a 10) para cada entrega individual.

### Portal da Diretoria (Administrador)
* **Login por Email** de administrador.
* **Dashboard principal** com estatísticas rápidas (total de alunos, professores e matérias).
* **Gerenciamento de Usuários:**
    * CRUD completo para **Alunos** (Nome, Email, RA, Senha).
    * CRUD completo para **Professores** (Nome, Email, Senha).
* **Gerenciamento Acadêmico:**
    * CRUD completo para **Matérias** (associando a um professor).
    * CRUD completo para **Turmas**.

## Tecnologias Utilizadas

* **Backend:** **Flask**
* **Banco de Dados:** **SQLite** (gerenciado via **Flask-SQLAlchemy**)
* **Autenticação:** Gerenciamento de sessão do Flask e senhas com hash (via **Werkzeug**)
* **Frontend:** HTML, CSS e JavaScript (conforme `index.html`)

## Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o SIGMA em sua máquina.

### 1. Pré-requisitos
* [Python 3.10+](https://www.python.org/downloads/)
* `pip` (gerenciador de pacotes do Python)

### 2. Instalação
1.  Clone este repositório:
    ```bash
    git clone https://seu-repositorio-aqui/sigma.git
    cd sigma
    ```
2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Instale as dependências necessárias:
    ```bash
    pip install Flask Flask-SQLAlchemy Werkzeug
    ```
    *(**Nota:** Em um projeto real, você criaria um `requirements.txt` com `pip freeze > requirements.txt`)*

### 3. Execução
1.  Execute o arquivo `app.py`:
    ```bash
    python app.py
    ```
2.  O Flask iniciará o servidor. O banco de dados `academico.db` será criado automaticamente no primeiro acesso.
3.  Acesse o sistema no seu navegador:
    **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

## Dados de Teste

Para facilitar os testes, utilize as credenciais abaixo (conforme definido em `index.html` e no script de popularização do banco de dados):

| Perfil | Usuário | Senha | Método de Login |
| :--- | :--- | :--- | :--- |
| **Aluno** | RA: `1234567` | `aluno123` | Preencher **apenas** o campo RA |
| **Professor**| Email: `professor@exemplo.com` | `prof123` | Preencher **apenas** o campo Email |
| **Diretoria**| Email: `diretor@exemplo.com` | `diretor123` | Preencher **apenas** o campo Email |

*(**Nota:** Os dados de teste acima precisam ser cadastrados no banco de dados para funcionar. O sistema de cadastro da Diretoria pode ser usado para criar essas contas.)*
