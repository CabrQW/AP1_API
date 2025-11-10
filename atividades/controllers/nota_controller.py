from flask import Blueprint, jsonify, request
from models import db
from models.nota import Nota
import requests  # comunicação síncrona entre microsserviços

nota_bp = Blueprint('nota_bp', __name__)

# Endpoints dos microsserviços
URL_ALUNOS = "http://gerenciamento:5001/api/alunos/"      # microsserviço de Alunos
URL_ATIVIDADES = "http://atividades:5002/api/atividades/"  # microsserviço de Atividades

# 🟢 CRIAR UMA NOVA NOTA
@nota_bp.route("/", methods=["POST"])
def criar_nota():
    """
    Cria uma nova nota
    ---
    tags:
      - Notas
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nota
            - aluno_id
            - atividade_id
          properties:
            nota:
              type: number
              example: 8.5
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 2
    responses:
      201:
        description: Nota criada com sucesso
      400:
        description: Erro ao criar nota
    """
    data = request.get_json()

    # valida aluno via microsserviço
    resp_aluno = requests.get(f"{URL_ALUNOS}{data['aluno_id']}")
    if resp_aluno.status_code != 200:
        return jsonify({"erro": "Aluno não encontrado"}), 400

    # valida atividade via microsserviço
    resp_atividade = requests.get(f"{URL_ATIVIDADES}{data['atividade_id']}")
    if resp_atividade.status_code != 200:
        return jsonify({"erro": "Atividade não encontrada"}), 400

    try:
        nova = Nota(
            nota=data["nota"],
            aluno_id=data["aluno_id"],
            atividade_id=data["atividade_id"]
        )
        db.session.add(nova)
        db.session.commit()
        return jsonify({"mensagem": "Nota criada com sucesso", "id": nova.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🟡 LISTAR TODAS AS NOTAS
@nota_bp.route("/", methods=["GET"])
def listar_notas():
    """
    Lista todas as notas
    ---
    tags:
      - Notas
    responses:
      200:
        description: Lista de notas cadastradas
    """
    notas = Nota.query.all()
    return jsonify([
        {
            "id": n.id,
            "nota": n.nota,
            "aluno_id": n.aluno_id,
            "atividade_id": n.atividade_id
        } for n in notas
    ]), 200


# 🔵 OBTER NOTA POR ID
@nota_bp.route("/<int:id>", methods=["GET"])
def obter_nota(id):
    """
    Obtém uma nota pelo ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: ID da nota
    responses:
      200:
        description: Nota encontrada
      404:
        description: Nota não encontrada
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404
    return jsonify({
        "id": nota.id,
        "nota": nota.nota,
        "aluno_id": nota.aluno_id,
        "atividade_id": nota.atividade_id
    }), 200


# 🟠 ATUALIZAR UMA NOTA
@nota_bp.route("/<int:id>", methods=["PUT"])
def atualizar_nota(id):
    """
    Atualiza uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            nota:
              type: number
              example: 9.0
            aluno_id:
              type: integer
              example: 1
            atividade_id:
              type: integer
              example: 2
    responses:
      200:
        description: Nota atualizada com sucesso
      404:
        description: Nota não encontrada
      400:
        description: Erro ao atualizar nota
    """
    data = request.get_json()
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404

    try:
        if "aluno_id" in data:
            resp_aluno = requests.get(f"{URL_ALUNOS}{data['aluno_id']}")
            if resp_aluno.status_code != 200:
                return jsonify({"erro": "Aluno não encontrado"}), 400
            nota.aluno_id = data["aluno_id"]

        if "atividade_id" in data:
            resp_atividade = requests.get(f"{URL_ATIVIDADES}{data['atividade_id']}")
            if resp_atividade.status_code != 200:
                return jsonify({"erro": "Atividade não encontrada"}), 400
            nota.atividade_id = data["atividade_id"]

        if "nota" in data:
            nota.nota = data["nota"]

        db.session.commit()
        return jsonify({"mensagem": "Nota atualizada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🔴 DELETAR UMA NOTA
@nota_bp.route("/<int:id>", methods=["DELETE"])
def deletar_nota(id):
    """
    Deleta uma nota pelo ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: ID da nota a ser deletada
    responses:
      200:
        description: Nota deletada com sucesso
      404:
        description: Nota não encontrada
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro": "Nota não encontrada"}), 404
    db.session.delete(nota)
    db.session.commit()
    return jsonify({"mensagem": "Nota deletada com sucesso"}), 200
