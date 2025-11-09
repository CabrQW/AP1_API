from flask import Blueprint, jsonify, request
from models import db
from models.reserva import Reserva
from datetime import date
import requests  # ✅ para validação via microserviço

reserva_bp = Blueprint("reserva_bp", __name__)

# 🟢 LISTAR TODAS AS RESERVAS
@reserva_bp.route("/", methods=["GET"])
def listar_reservas():
    """
    Lista todas as reservas
    ---
    tags:
      - Reservas
    responses:
      200:
        description: Lista de reservas
        examples:
          application/json: [
            {"id": 1, "num_sala": "101", "lab": false, "data": "2025-11-20", "turma_id": 2}
          ]
    """
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas]), 200


# 🟡 OBTER RESERVA POR ID
@reserva_bp.route("/<int:id>", methods=["GET"])
def obter_reserva(id):
    """
    Retorna uma reserva específica pelo ID
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Reserva encontrada
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404
    return jsonify(reserva.to_dict()), 200


# 🔵 CRIAR UMA NOVA RESERVA
@reserva_bp.route("/", methods=["POST"])
def criar_reserva():
    """
    Cria uma nova reserva
    ---
    tags:
      - Reservas
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - num_sala
            - data
            - turma_id
          properties:
            num_sala:
              type: string
              example: "105"
            lab:
              type: boolean
              example: true
            data:
              type: string
              format: date
              example: "2025-11-20"
            turma_id:
              type: integer
              example: 3
    responses:
      201:
        description: Reserva criada com sucesso
      400:
        description: Erro ao criar a reserva
    """
    dados = request.get_json()

    # ✅ valida se a turma existe via microserviço gerenciamento
    try:
        turma_id = dados["turma_id"]
        resp = requests.get(f"http://gerenciamento:5001/api/turmas/{turma_id}")
        if resp.status_code != 200:
            return jsonify({"erro": "Turma não encontrada"}), 404
    except KeyError:
        return jsonify({"erro": "Campo 'turma_id' é obrigatório"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": f"Erro ao validar turma: {str(e)}"}), 500

    try:
        nova_reserva = Reserva(
            num_sala=dados["num_sala"],
            lab=dados.get("lab", False),
            data=date.fromisoformat(dados["data"]),
            turma_id=turma_id
        )
        db.session.add(nova_reserva)
        db.session.commit()
        return jsonify(nova_reserva.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🟠 ATUALIZAR UMA RESERVA
@reserva_bp.route("/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    """
    Atualiza uma reserva existente
    ---
    tags:
      - Reservas
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            num_sala:
              type: string
              example: "101"
            lab:
              type: boolean
              example: false
            data:
              type: string
              format: date
              example: "2025-11-25"
            turma_id:
              type: integer
              example: 2
    responses:
      200:
        description: Reserva atualizada com sucesso
      404:
        description: Reserva não encontrada
    """
    dados = request.get_json()
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    # ✅ valida turma se estiver atualizando
    if "turma_id" in dados:
        try:
            resp = requests.get(f"http://gerenciamento:5001/api/turmas/{dados['turma_id']}")
            if resp.status_code != 200:
                return jsonify({"erro": "Turma não encontrada"}), 404
        except requests.exceptions.RequestException as e:
            return jsonify({"erro": f"Erro ao validar turma: {str(e)}"}), 500

    try:
        reserva.num_sala = dados.get("num_sala", reserva.num_sala)
        reserva.lab = dados.get("lab", reserva.lab)
        if "data" in dados:
            reserva.data = date.fromisoformat(dados["data"])
        reserva.turma_id = dados.get("turma_id", reserva.turma_id)

        db.session.commit()
        return jsonify(reserva.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


# 🔴 DELETAR UMA RESERVA
@reserva_bp.route("/<int:id>", methods=["DELETE"])
def deletar_reserva(id):
    """
    Exclui uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Reserva excluída com sucesso
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"mensagem": "Reserva deletada com sucesso"}), 200
