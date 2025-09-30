import os
from flask import Flask, request, jsonify
from flask.json.provider import DefaultJSONProvider
from flasgger import Swagger
from datetime import datetime, date
from models import db
from config import Config
from models.aluno import Aluno
from models.turma import Turma
from models.professor import Professor

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)
app.json = CustomJSONProvider(app)

Swagger(app)

db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/api/alunos', methods=['GET'])
def api_list_alunos():
    """
    Lista todos os alunos.
    ---
    tags:
      - Alunos
    description: Retorna todos os alunos cadastrados em JSON
    produces:
      - application/json
    responses:
      200:
        description: Lista de alunos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: João da Silva
              idade:
                type: integer
                example: 15
              data_nascimento:
                type: string
                format: date
                example: 2010-05-12
              nota_primeiro_semestre:
                type: number
                example: 7.5
              nota_segundo_semestre:
                type: number
                example: 8.0
              media_final:
                type: number
                example: 7.75
              turma_id:
                type: integer
                example: 2
              turma:
                type: string
                example: Turma A
    """
    alunos = Aluno.query.all()
    resultado = [
        {
            'id': a.id,
            'nome': a.nome,
            'idade': a.idade,
            'data_nascimento': a.data_nascimento,
            'nota_primeiro_semestre': a.nota_primeiro_semestre,
            'nota_segundo_semestre': a.nota_segundo_semestre,
            'media_final': a.media_final,
            'turma_id': a.turma_id,
            'turma': a.turma.descricao if a.turma else None
        }
        for a in alunos
    ]
    return jsonify(resultado), 200


# POST Aluno
@app.route('/api/alunos', methods=['POST'])
def api_create_aluno():
    """
    Cria um novo aluno.
    ---
    tags:
      - Alunos
    description: Cria um aluno com JSON
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: aluno
        description: Objeto JSON com os dados do aluno
        required: true
        schema:
          type: object
          required:
            - nome
            - idade
            - turma_id
          properties:
            nome:
              type: string
              example: João da Silva
            idade:
              type: integer
              example: 15
            data_nascimento:
              type: string
              example: 2010-05-12
            nota_primeiro_semestre:
              type: number
              example: 7.5
            nota_segundo_semestre:
              type: number
              example: 8.0
            media_final:
              type: number
              example: 7.75
            turma_id:
              type: integer
              example: 2
    responses:
      201:
        description: Aluno criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: João da Silva
      400:
        description: Requisição inválida
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Campos obrigatórios faltando"
    """
    dados = request.get_json()

    if not dados or not all(k in dados for k in ('nome', 'idade', 'turma_id')):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    turma = Turma.query.get(dados['turma_id'])
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    data_nasc = None
    if 'data_nascimento' in dados and dados['data_nascimento']:
        data_nasc = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()

    novo_aluno = Aluno(
        nome=dados['nome'],
        idade=dados['idade'],
        turma_id=dados['turma_id'],
        data_nascimento=data_nasc,
        nota_primeiro_semestre=dados.get('nota_primeiro_semestre'),
        nota_segundo_semestre=dados.get('nota_segundo_semestre'),
        media_final=dados.get('media_final')
    )
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({
        'id': novo_aluno.id,
        'nome': novo_aluno.nome,
        'data_nascimento': novo_aluno.data_nascimento
    }), 201


@app.route('/api/alunos/<int:id>', methods=['PUT'])
def api_update_aluno(id):
    """
    Atualiza um aluno existente pelo ID.
    ---
    tags:
      - Alunos
    description: Atualiza os dados do aluno
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do aluno a ser atualizado
      - in: body
        name: aluno
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João da Silva
            idade:
              type: integer
              example: 15
            data_nascimento:
              type: string
              format: date
              example: 2010-05-12
            nota_primeiro_semestre:
              type: number
              example: 7.5
            nota_segundo_semestre:
              type: number
              example: 8.0
            media_final:
              type: number
              example: 7.75
            turma_id:
              type: integer
              example: 2
    responses:
      200:
        description: Aluno atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: João da Silva
            data_nascimento:
              type: string
              format: date
              example: 2010-05-12
      400:
        description: Erro na atualização
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Aluno não encontrado ou dados inválidos"
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    dados = request.get_json()
    aluno.nome = dados.get('nome', aluno.nome)
    aluno.idade = dados.get('idade', aluno.idade)

    if 'data_nascimento' in dados and dados['data_nascimento']:
        aluno.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()

    aluno.nota_primeiro_semestre = dados.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    aluno.nota_segundo_semestre = dados.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.media_final = dados.get('media_final', aluno.media_final)

    if 'turma_id' in dados:
        turma = Turma.query.get(dados['turma_id'])
        if not turma:
            return jsonify({"error": "Turma não encontrada"}), 404
        aluno.turma_id = dados['turma_id']

    db.session.commit()

    return jsonify({
        'id': aluno.id,
        'nome': aluno.nome,
        'data_nascimento': aluno.data_nascimento
    }), 200


@app.route('/api/alunos/<int:id>', methods=['DELETE'])
def api_delete_aluno(id):
    """
    Deleta um aluno existente pelo ID.
    ---
    tags:
      - Alunos
    description: Remove um aluno pelo ID
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do aluno a ser removido
    responses:
      200:
        description: Aluno deletado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Aluno deletado com sucesso"
      404:
        description: Aluno não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Aluno não encontrado"
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"message": "Aluno deletado com sucesso"}), 200

@app.route('/api/professores', methods=['GET'])
def api_list_professores():
    """
    Lista todos os professores.
    ---
    tags:
      - Professores
    produces:
      - application/json
    responses:
      200:
        description: Lista de professores
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nome:
                type: string
                example: João da Silva
              idade:
                type: integer
                example: 40
              materia:
                type: string
                example: Matemática
              observacao:
                type: string
                example: Professor com experiência em ensino médio
              turmas:
                type: array
                items:
                  type: string
                  example: Turma A
    """
    professores = Professor.query.all()
    resultado = [
        {
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'materia': p.materia,
            'observacao': p.observacao,
            'turmas': [t.nome for t in p.turmas] if hasattr(p, 'turmas') else []
        }
        for p in professores
    ]
    return jsonify(resultado), 200

@app.route('/api/professores', methods=['POST'])
def api_create_professor():
    """
    Cria um novo professor.
    ---
    tags:
      - Professores
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: professor
        required: true
        schema:
          type: object
          required:
            - nome
            - idade
            - materia
          properties:
            nome:
              type: string
              example: João da Silva
            idade:
              type: integer
              example: 40
            materia:
              type: string
              example: Matemática
            observacao:
              type: string
              example: Professor com experiência em ensino médio
    responses:
      201:
        description: Professor criado com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Professor criado
            id:
              type: integer
              example: 1
    """
    dados = request.get_json()
    novo = Professor(
        nome=dados['nome'],
        idade=dados['idade'],
        materia=dados['materia'],
        observacao=dados.get('observacao')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Professor criado', 'id': novo.id}), 201

@app.route('/api/professores/<int:id>', methods=['PUT'])
def api_update_professor(id):
    """
    Atualiza um professor existente.
    ---
    tags:
      - Professores
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: professor
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João da Silva
            idade:
              type: integer
              example: 41
            materia:
              type: string
              example: Física
            observacao:
              type: string
              example: Atualização de observações
    responses:
      200:
        description: Professor atualizado com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Professor atualizado.
    """
    prof = Professor.query.get_or_404(id)
    dados = request.get_json()
    prof.nome = dados.get('nome', prof.nome)
    prof.idade = dados.get('idade', prof.idade)
    prof.materia = dados.get('materia', prof.materia)
    prof.observacao = dados.get('observacao', prof.observacao)
    db.session.commit()
    return jsonify({'mensagem': 'Professor atualizado.'})

@app.route('/api/professores/<int:id>', methods=['DELETE'])
def api_delete_professor(id):
    """
    Deleta um professor existente.
    ---
    tags:
      - Professores
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Professor deletado com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Professor deletado.
    """
    prof = Professor.query.get_or_404(id)
    db.session.delete(prof)
    db.session.commit()
    return jsonify({'mensagem': 'Professor deletado.'})


@app.route('/api/turmas', methods=['GET'])
def api_list_turmas():
    """
    Lista todas as turmas.
    ---
    tags:
      - Turmas
    description: Retorna todas as turmas cadastradas em JSON
    produces:
      - application/json
    responses:
      200:
        description: Lista de turmas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              descricao:
                type: string
                example: Turma A
              professor_id:
                type: integer
                example: 2
              professor:
                type: string
                example: João da Silva
    """
    turmas = Turma.query.all()
    resultado = [
        {
            'id': t.id,
            'descricao': t.descricao,
            'professor_id': t.professor_id,
            'professor': t.professor.nome if t.professor else None
        }
        for t in turmas
    ]
    return jsonify(resultado), 200


@app.route('/api/turmas', methods=['POST'])
def api_create_turma():
    """
    Cria uma nova turma.
    ---
    tags:
      - Turmas
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: turma
        description: Objeto JSON com os dados da turma
        required: true
        schema:
          type: object
          required:
            - descricao
            - professor_id
          properties:
            descricao:
              type: string
              example: Turma B
            professor_id:
              type: integer
              example: 2
    responses:
      201:
        description: Turma criada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Turma criada
            id:
              type: integer
              example: 3
      400:
        description: Requisição inválida
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Campos obrigatórios faltando"
    """
    dados = request.get_json()
    if not dados or not all(k in dados for k in ('descricao', 'professor_id')):
        return jsonify({"error": "Campos obrigatórios faltando"}), 400

    professor = Professor.query.get(dados['professor_id'])
    if not professor:
        return jsonify({"error": "Professor não encontrado"}), 404

    nova_turma = Turma(
        descricao=dados['descricao'],
        professor_id=dados['professor_id']
    )
    db.session.add(nova_turma)
    db.session.commit()

    return jsonify({
        'mensagem': 'Turma criada',
        'id': nova_turma.id
    }), 201


@app.route('/api/turmas/<int:id>', methods=['PUT'])
def api_update_turma(id):
    """
    Atualiza uma turma existente pelo ID.
    ---
    tags:
      - Turmas
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da turma a ser atualizada
      - in: body
        name: turma
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: Turma C
            professor_id:
              type: integer
              example: 3
    responses:
      200:
        description: Turma atualizada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Turma atualizada"
      404:
        description: Turma não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Turma não encontrada"
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    dados = request.get_json()
    if 'descricao' in dados:
        turma.descricao = dados['descricao']
    if 'professor_id' in dados:
        professor = Professor.query.get(dados['professor_id'])
        if not professor:
            return jsonify({"error": "Professor não encontrado"}), 404
        turma.professor_id = dados['professor_id']

    db.session.commit()

    return jsonify({'mensagem': 'Turma atualizada'}), 200


@app.route('/api/turmas/<int:id>', methods=['DELETE'])
def api_delete_turma(id):
    """
    Remove uma turma existente pelo ID.
    ---
    tags:
      - Turmas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da turma a ser removida
    responses:
      200:
        description: Turma removida com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: "Turma deletada"
      404:
        description: Turma não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Turma não encontrada"
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({"error": "Turma não encontrada"}), 404

    db.session.delete(turma)
    db.session.commit()
    return jsonify({'mensagem': 'Turma deletada'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)