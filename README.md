## Integrates do grupo

<p>Guilherme Oliveira Reis</p>
<p>Carlos Eduardo da Costa Viana</p>
<p>Filipe Machado Souza</p>

# API Flask — Gerenciamento de Professores, Turmas e Alunos

Projeto: API REST completa em Flask (estrutura MVC sem views) para gerenciar Professores, Turmas e Alunos.

---

## Sumário

* [Descrição](#descri%C3%A7%C3%A3o)
* [Funcionalidades](#funcionalidades)
* [Arquitetura e organização do código](#arquitetura-e-organiza%C3%A7%C3%A3o-do-c%C3%B3digo)
* [Pré-requisitos](#pr%C3%A9-requisitos)
* [Instalação e execução local](#instala%C3%A7%C3%A3o-e-execu%C3%A7%C3%A3o-local)
* [Banco de dados](#banco-de-dados)
* [Documentação da API (Swagger)](#documenta%C3%A7%C3%A3o-da-api-swagger)
* [Docker (conteinerização)](#docker-conteineriza%C3%A7%C3%A3o)
* [Controle de versão](#controle-de-vers%C3%A3o)
* [Boas práticas e considerações](#boas-pr%C3%A1ticas-e-considera%C3%A7%C3%B5es)
* [Endpoints principais](#endpoints-principais)
* [Exemplos de requests (curl)](#exemplos-de-requests-curl)

---

## Descrição

API REST construída com Flask para realizar operações CRUD (GET, POST, PUT, DELETE) sobre as entidades **Professor**, **Turma** e **Aluno**. Persistência em SQLite via SQLAlchemy. Documentação automática via **Flasgger** (Swagger). A aplicação foi pensada em uma estrutura tipo MVC (Model, Controller/Routes e Config) — sem views, pois é uma API.

## Funcionalidades

* CRUD completo para Professores, Turmas e Alunos.
* Relacionamentos entre entidades (ex.: Aluno pertence a Turma; Turma tem Professor).
* Validações básicas (ex.: verificar existência de professor/turma antes de criar relacionamento).
* Documentação interativa (Swagger / Flasgger).
* Serialização customizada de `date` para `YYYY-MM-DD`.
* Suporte a conteinerização com Docker.

## Arquitetura e organização do código

Estrutura sugerida do projeto (exemplo):

```
AP1-API/
├── app.py
├── config.py
├── models/
│   ├── __init__.py    # instancia db = SQLAlchemy()
│   ├── aluno.py       # model Aluno
│   ├── turma.py       # model Turma
│   └── professor.py   # model Professor
├── controllers/       # opcional, aqui iriam as rotas em módulos separados
│   ├── alunos.py
│   ├── turmas.py
│   └── professores.py
├── requirements.txt
├── Dockerfile
└── README.md
```

* **Models**: definem as tabelas e relacionamentos usando SQLAlchemy.
* **app.py**: inicializa Flask, registra rotas (controllers) e configura Swagger. No seu `app.py` há também um `CustomJSONProvider` para formatar datas.
* **controllers**: (opcional) separar cada grupo de rotas em arquivos para organização.
* **migrations**: caso use Flask-Migrate/Alembic para versionamento do esquema do banco.

## Pré-requisitos

* Python 3.9+ (recomendado)
* pip
* Docker (para conteinerizar)

## Instalação e execução local

1. Clone o repositório:

```bash
git clone https://github.com/CabrQW/AP1_API.git
cd seu-repo
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

3. Instale dependências (exemplo de `requirements.txt`):

```text
Flask
Flask-SQLAlchemy
flasgger
python-dotenv
```

Instale com:

```bash
pip install -r requirements.txt
```

4. Variáveis de ambiente (opcional):

Crie um arquivo `.env` (se estiver usando python-dotenv) ou exporte variáveis diretamente. Um `Config` simples pode usar `SQLALCHEMY_DATABASE_URI` apontando para SQLite:

```py
# config.py (exemplo)
import os
from pathlib import Path
BASE_DIR = Path(__file__).parent
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "app.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

5. Inicialize o banco e execute a aplicação:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # opcional
python app.py
```

Por padrão o `app.py` do exemplo roda em `http://localhost:5000`.

## Banco de dados

* O projeto usa SQLite por padrão (arquivo `app.db` no root).
* No `app.py` do exemplo você tem `db.create_all()` dentro do `app.app_context()` para criar as tabelas automaticamente.

### Usando migrations (opcional, recomendado para projetos reais)

Se preferir usar Alembic/Flask-Migrate:

```bash
pip install Flask-Migrate
```

No `app.py`/`__init__` do pacote, inicialize o Migrate:

```py
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

Comandos:

```bash
flask db init
flask db migrate -m "create tables"
flask db upgrade
```

## Documentação da API (Swagger)

Este projeto utiliza **Flasgger** para gerar a documentação Swagger a partir das docstrings dos endpoints (como no `app.py` que você enviou).

* Após subir a aplicação localmente, a UI do Swagger normalmente estará disponível em:

```
http://127.0.0.1:5000/apidocs/
```

ou dependendo da versão/rota do Flasgger, em `/apidocs` ou `/apidocs/index.html`.

No seu `app.py` já há `Swagger(app)` e docstrings nos endpoints — isso gera a documentação automática.

## Docker (conteinerização)

Exemplo mínimo de `Dockerfile`:

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["python", "app.py"]
```

Construir e rodar a imagem:

```bash
docker build -t minha-api-flask .
docker run -p 5000:5000 minha-api-flask
```

Exemplo `docker-compose.yml` (opcional):

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
```

Observação: para persistir o arquivo sqlite entre execuções com Docker, monte um volume:

```bash
docker run -v $(pwd)/data:/app -p 5000:5000 minha-api-flask
```

ou no `docker-compose` use `volumes`.

## Controle de versão (GitHub)

* Faça commits pequenos e com mensagens descritivas (ex.: `feat: add aluno CRUD`, `fix: validate turma existence on aluno create`, `chore: add Dockerfile`).
* Tenha um `.gitignore` incluindo `.venv/`, `__pycache__/`, `*.pyc`, `app.db` (a não ser que queira commitar o DB), `.env`.

Exemplo de fluxo:

```bash
git init
git add .
git commit -m "chore: projeto inicial com models e endpoints básicos"
git branch -M main
git remote add origin git@github.com:seu-usuario/seu-repo.git
git push -u origin main
```

## Boas práticas e considerações

* Separe rotas em blueprints ou módulos `controllers` para facilitar manutenção.
* Trate erros de forma consistente (erro 400/404/500) e devolva mensagens padronizadas em JSON.
* Valide e faça sanitização dos dados de entrada (use Marshmallow, Pydantic ou validações manuais).
* Em produção, não rode Flask com `debug=True`. Use um WSGI server (Gunicorn/uvicorn) e um proxy reverso (NGINX) se necessário.
* Considere usar testes automatizados (pytest) para endpoints e modelos.

## Endpoints principais

> Abaixo está um resumo dos endpoints já implementados no seu `app.py` (descrições resumidas):

* `GET /api/alunos` — lista alunos

* `POST /api/alunos` — cria aluno

* `PUT /api/alunos/<id>` — atualiza aluno

* `DELETE /api/alunos/<id>` — deleta aluno

* `GET /api/professores` — lista professores

* `POST /api/professores` — cria professor

* `PUT /api/professores/<id>` — atualiza professor

* `DELETE /api/professores/<id>` — deleta professor

* `GET /api/turmas` — lista turmas

* `POST /api/turmas` — cria turma

* `PUT /api/turmas/<id>` — atualiza turma

* `DELETE /api/turmas/<id>` — deleta turma

(As docstrings em `app.py` são usadas para ampliar cada operação na UI do Swagger.)

## Exemplos de requests (curl)

Criar professor:

```bash
curl -X POST http://127.0.0.1:5000/api/professores \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","idade":40,"materia":"Matemática"}'
```

Criar turma:

```bash
curl -X POST http://127.0.0.1:5000/api/turmas \
  -H "Content-Type: application/json" \
  -d '{"descricao":"Turma A","professor_id":1}'
```

Criar aluno:

```bash
curl -X POST http://127.0.0.1:5000/api/alunos \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria","idade":15,"turma_id":1}'
```

## Próximos passos sugeridos

* Separar rotas em Blueprints (`controllers/`) para melhor organização.
* Adicionar validação com Marshmallow (serialização/validação).
* Implementar Flask-Migrate para versionamento de banco.
* Adicionar testes automatizados e CI (ex.: GitHub Actions).

---

Se quiser, gero também:

* `requirements.txt` pronto com as versões mais compatíveis;
* `Dockerfile` e `docker-compose.yml` completos (já tem um exemplo acima, posso gerar arquivo real);
* arquivos de `models/` (aluno.py, turma.py, professor.py) baseados no que seu `app.py` espera;
* separar as rotas em `controllers/` (blueprints) e ajustar `app.py` para registrar blueprints.

Quer que eu adicione algum desses arquivos agora?
