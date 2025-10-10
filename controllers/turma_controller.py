from flask import request, jsonify
from app import db
from models.turma import Turma
from models.aluno import Aluno

def registrar_rotas_turmas(app):

    @app.route('/api/turmas', methods=['GET'])
    def listar_turmas():
        turmas = Turma.query.all()
        resultado = [
            {
                'id': t.id,
                'descricao': t.descricao,
                'professor_id': t.professor_id,
                'ativo': t.ativo,
                'professor': t.professor.nome if t.professor else None,
                'alunos': [a.nome for a in t.alunos]
            }
            for t in turmas
        ]
        return jsonify(resultado)

    @app.route('/api/turmas', methods=['POST'])
    def criar_turma():
        dados = request.get_json()
        nova_turma = Turma(
            descricao=dados['descricao'],
            ativo=dados.get('ativo', True),
            professor_id=dados['professor_id']
        )

        if 'alunos' in dados:
            alunos = Aluno.query.filter(Aluno.id.in_(dados['alunos'])).all()
            nova_turma.alunos = alunos

        db.session.add(nova_turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma criada', 'id': nova_turma.id}), 201

    @app.route('/api/turmas/<int:id>', methods=['PUT'])
    def atualizar_turma(id):
        turma = Turma.query.get_or_404(id)
        dados = request.get_json()

        turma.descricao = dados.get('descricao', turma.descricao)
        turma.ativo = dados.get('ativo', turma.ativo)
        if 'professor_id' in dados:
            turma.professor_id = dados['professor_id']
        if 'alunos' in dados:
            alunos = Aluno.query.filter(Aluno.id.in_(dados['alunos'])).all()
            turma.alunos = alunos

        db.session.commit()
        return jsonify({'mensagem': 'Turma atualizada.'})

    @app.route('/api/turmas/<int:id>', methods=['DELETE'])
    def deletar_turma(id):
        turma = Turma.query.get_or_404(id)
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma deletada.'})