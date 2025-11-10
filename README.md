🏫 Projeto API Escolar - Microsserviços
📖 Descrição do Projeto

Este projeto consiste em três microsserviços independentes que formam um ecossistema de gestão escolar:

Gerenciamento – Gerencia alunos, professores e turmas.

Atividades – Gerencia atividades acadêmicas e notas de alunos.

Reservas – Gerencia reservas de salas e laboratórios para turmas.

Cada microsserviço possui sua própria API RESTful, banco de dados independente e documentação Swagger para facilitar testes e integração.
A comunicação entre os serviços é síncrona, utilizando a biblioteca requests do Python.

🏗 Arquitetura do Projeto

Microsserviços independentes e autônomos

Banco de dados individual para cada serviço (SQLite ou PostgreSQL)

Comunicação síncrona com requests

Flask + SQLAlchemy para rotas e persistência

Swagger para documentação interativa

Fluxo de integração:

Atividades valida IDs de Turma e Professor no microsserviço de Gerenciamento.

Notas valida IDs de Aluno no microsserviço de Gerenciamento e de Atividade no microsserviço de Atividades.

Reservas valida IDs de Turma no microsserviço de Gerenciamento.

📂 Estrutura de Pastas
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

📌 Documentação Swagger

Cada microsserviço possui Swagger integrado via docstrings do Flask:

Reservas: http://localhost:5000/apidocs

Gerenciamento: http://localhost:5001/apidocs

Atividades: http://localhost:5002/apidocs

Exemplo de docstring Swagger para criação de atividade:

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

🐳 Executando com Docker
Pré-requisitos

Docker Desktop

Python 3.11+

1️⃣ Criar docker-compose.yml
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

2️⃣ Build dos containers
docker-compose build

3️⃣ Subir os microsserviços
docker-compose up

4️⃣ Acessar os serviços

Reservas: http://localhost:5000/

Gerenciamento: http://localhost:5001/

Atividades: http://localhost:5002/
Swagger estará disponível nos endpoints /swagger de cada serviço.

🔗 Integração entre microsserviços

Exemplo de requisição síncrona usando requests:

import requests

# Verificar se a turma existe antes de criar atividade
res = requests.get(f"http://localhost:5000/turmas/{turma_id}")
if res.status_code != 200:
    raise Exception("Turma não encontrada")


Atividades consulta Gerenciamento (Turmas e Professores)

Notas consulta Gerenciamento (Alunos) e Atividades (Atividades)

Reservas consulta Gerenciamento (Turmas)

📦 Requisitos Python (requirements.txt)
Flask==2.3.3
Flask-SQLAlchemy==3.0.4
requests==2.32.0
flasgger==1.9.5

⚡ Observações

Cada serviço pode ser executado independentemente para testes locais.

Arquitetura síncrona simples

Swagger permite testar todas as rotas de forma interativa.
