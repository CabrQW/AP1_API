from flask import Blueprint, jsonify, request
from models import db
from models.atividade import Atividade
from datetime import datetime
import requests  # para comunicação síncrona entre microsserviços

atividade_bp = Blueprint('atividade_bp', __name__)

# Endpoints dos microsserviços
URL_TURMAS = "http://gerenciamento:5001/api/turmas/"      # microsserviço de Turmas
URL_PROFESSORES = "http://gerenciamento:5001/api/professores/"  # microsserviço de Professores

# 🟢 Criar uma nova atividade
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
        description: Dados da nova atividade
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
            descricao:
              type: string
              example: "Trabalho sobre Flask e SQLAlchemy"
            peso_porcento:
              type: number
              example: 30
            data_entrega:
              type: string
              format: date
              example: "2025-11-20"
            turma_id:
              type: integer
              example: 3
            professor_id:
              type: integer
              example: 2
    responses:
      201:
        description: Atividade criada com sucesso
      400:
        description: Erro ao criar a atividade
    """
    data = request.get_json()
    
    # ✅ Validação via microsserviço de Turmas
    resp_turma = requests.get(f"{URL_TURMAS}{data['turma_id']}")
    if resp_turma.status_code != 200:
        return jsonify({"erro": f"Turma com ID {data['turma_id']} não encontrada"}), 400

    # ✅ Validação via microsserviço de Professores
    resp_prof = requests.get(f"{URL_PROFESSORES}{data['professor_id']}")
    if resp_prof.status_code != 200:
        return jsonify({"erro": f"Professor com ID {data['professor_id']} não encontrado"}), 400

    try:
        nova = Atividade(
            nome_atividade=data['nome_atividade'],
            descricao=data.get('descricao', ''),
            peso_porcento=data['peso_porcento'],
            data_entrega=datetime.strptime(data['data_entrega'], "%Y-%m-%d").date(),
            turma_id=data['turma_id'],
            professor_id=data['professor_id']
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify(nova.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🟡 Listar todas as atividades
@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    """
    Lista todas as atividades
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Lista de atividades
    """
    atividades = Atividade.query.all()
    return jsonify([a.to_dict() for a in atividades])


# 🔵 Obter uma atividade por ID
@atividade_bp.route('/<int:id>', methods=['GET'])
def obter_atividade(id):
    """
    Obtém uma atividade pelo ID
    ---
    tags:
      - Atividades
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da atividade
    responses:
      200:
        description: Atividade encontrada
      404:
        description: Atividade não encontrada
    """
    atividade = Atividade.query.get(id)
    if atividade:
        return jsonify(atividade.to_dict())
    return jsonify({"erro": "Atividade não encontrada"}), 404


# 🟠 Atualizar uma atividade
@atividade_bp.route('/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    """
    Atualiza uma atividade existente
    ---
    tags:
      - Atividades
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        description: Dados atualizados da atividade
        required: true
        schema:
          type: object
          properties:
            nome_atividade:
              type: string
            descricao:
              type: string
            peso_porcento:
              type: number
            data_entrega:
              type: string
              format: date
            turma_id:
              type: integer
            professor_id:
              type: integer
    responses:
      200:
        description: Atividade atualizada com sucesso
      404:
        description: Atividade não encontrada
    """
    data = request.get_json()
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404

    try:
        # Validação via microsserviço
        if 'turma_id' in data:
            resp_turma = requests.get(f"{URL_TURMAS}{data['turma_id']}")
            if resp_turma.status_code != 200:
                return jsonify({"erro": f"Turma com ID {data['turma_id']} não encontrada"}), 400
            atividade.turma_id = data['turma_id']

        if 'professor_id' in data:
            resp_prof = requests.get(f"{URL_PROFESSORES}{data['professor_id']}")
            if resp_prof.status_code != 200:
                return jsonify({"erro": f"Professor com ID {data['professor_id']} não encontrado"}), 400
            atividade.professor_id = data['professor_id']

        atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
        atividade.descricao = data.get('descricao', atividade.descricao)
        atividade.peso_porcento = data.get('peso_porcento', atividade.peso_porcento)
        if 'data_entrega' in data:
            atividade.data_entrega = datetime.strptime(data['data_entrega'], "%Y-%m-%d").date()

        db.session.commit()
        return jsonify(atividade.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🔴 Deletar uma atividade
@atividade_bp.route('/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    """
    Deleta uma atividade pelo ID
    ---
    tags:
      - Atividades
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        description: ID da atividade
    responses:
      204:
        description: Atividade deletada com sucesso
      404:
        description: Atividade não encontrada
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"mensagem": "Atividade deletada com sucesso"}), 204
