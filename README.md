Projeto API Escolar - Microsserviços
Descrição do Projeto

Este projeto consiste em três microsserviços que formam um ecossistema de gestão escolar:

Gerenciamento – Gerencia alunos, professores e turmas.

Atividades – Gerencia atividades acadêmicas e notas de alunos.

Reservas – Gerencia reservas de salas e laboratórios para turmas.

Cada microsserviço é independente, possui seu próprio banco de dados e endpoints RESTful. A comunicação entre serviços é realizada de forma síncrona, utilizando a biblioteca requests do Python.

A documentação de cada serviço é disponibilizada via Swagger, permitindo testar endpoints e entender os parâmetros e respostas de cada API.

Arquitetura do Projeto

Microsserviços independentes: Cada serviço é autônomo e gerencia suas próprias responsabilidades.

Banco de dados: Cada serviço possui seu próprio banco SQL (SQLite ou PostgreSQL configurável).

Comunicação entre microsserviços: Síncrona usando requests.

Flask + SQLAlchemy: Para gerenciamento de rotas e persistência de dados.

Swagger: Documentação e teste de APIs integrado via docstrings.

Fluxo de integração:

Atividades valida IDs de Turma e Professor do microsserviço de Gerenciamento.

Notas valida IDs de Aluno e Atividade do microsserviço correspondente.

Reservas valida IDs de Turma do microsserviço de Gerenciamento.

Estrutura de Pastas
AP1_API/
├─ atividades/
│  ├─ controllers/
│  ├─ models/
│  ├─ app.py
│  ├─ requirements.txt
├─ reservas/
│  ├─ controllers/
│  ├─ models/
│  ├─ app.py
│  ├─ requirements.txt
├─ gerenciamento/
│  ├─ controllers/
│  ├─ models/
│  ├─ app.py
│  ├─ requirements.txt
├─ docker-compose.yml
└─ README.md

Documentação Swagger

Cada microsserviço possui Swagger integrado via docstrings:

Gerenciamento: /swagger

Atividades: /swagger

Reservas: /swagger

Exemplo de rota documentada em Swagger:

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    """
    Cria uma nova atividade
    ---
    tags:
      - Atividades
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome_atividade
            - peso_porcento
            - data_entrega
            - turma_id
            - professor_id
          properties:
            nome_atividade:
              type: string
              example: "Trabalho Final"
    responses:
      201:
        description: Atividade criada com sucesso
      400:
        description: Erro ao criar a atividade
    """

Executando os microsserviços com Docker
Pré-requisitos

Docker Desktop

Python 3.11+

Passos

No diretório raiz (AP1_API/), crie o docker-compose.yml com:

services:
  gerenciamento:
    build: ./gerenciamento
    container_name: gerenciamento
    ports:
      - "5000:5000"
  atividades:
    build: ./atividades
    container_name: atividades
    ports:
      - "5001:5000"
  reservas:
    build: ./reservas
    container_name: reservas
    ports:
      - "5002:5000"


Buildar os containers:

docker-compose build


Subir os serviços:

docker-compose up


Acessar as APIs via:

http://localhost:5000 – Gerenciamento

http://localhost:5001 – Atividades

http://localhost:5002 – Reservas

Swagger estará disponível nos endpoints /swagger de cada serviço.

Integração entre microsserviços

Atividades precisa consultar Turmas e Professores em Gerenciamento.

Notas valida se Aluno existe em Gerenciamento e se Atividade existe em Atividades.

Reservas valida se Turma existe em Gerenciamento.

Exemplo de requisição entre microsserviços usando requests:

import requests

# Verificar se a turma existe antes de criar atividade
res = requests.get(f"http://localhost:5000/turmas/{turma_id}")
if res.status_code != 200:
    raise Exception("Turma não encontrada")

Requisitos Python

requirements.txt padrão para cada serviço:

Flask==2.3.3
Flask-SQLAlchemy==3.0.4
requests==2.32.0
flasgger==1.9.5

Observações

Cada serviço pode ser executado de forma independente para testes locais.

Cada microsserviço possui Swagger para facilitar documentação e testes de endpoints.

Arquitetura síncrona simples, sem Celery ou Redis, garantindo fácil entendimento e deploy local.
