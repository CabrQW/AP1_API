## Integrates do grupo

<p>Guilherme Oliveira Reis</p>
<p>Carlos Eduardo da Costa Viana</p>
<p>Filipe Machado Souza</p>

## Descrição do Projeto
API construída em Flask, estruturada no padrão MVC, que permite o gerenciamento de Professores, Turmas e Alunos.  
O projeto utiliza SQLite como banco de dados, ORM SQLAlchemy, e documentação via Swagger.

## Como rodar localmente (sem Docker)
1. Criar e ativar um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # Linux/Mac

2. Instalar as dependências:
   
   pip install -r requirements.txt

3. Rodar a aplicação:

   python app.py

## Rodando com Docker

1. Construir a imagem:

   docker build -t flask-api .	

2. Rodar o container:

   docker run -d -p 5000:5000 flask-api

3. A API estará disponível em http://localhost:5000