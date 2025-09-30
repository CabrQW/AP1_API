from flask import request, jsonify
from app import db
from models.aluno import Aluno
from models.turma import Turma
from datetime import datetime

def registrar_rotas_alunos(app):

    @app.route('/alunos', methods=['GET'])
    def listar_alunos():
        alunos = Aluno.query.all()
        resultado = [
            {
                'id': a.id,
                'nome': a.nome,
                'idade': a.idade,
                'data_nascimento': a.data_nascimento.strftime('%Y-%m-%d') if a.data_nascimento else None,
                'nota_primeiro_semestre': a.nota_primeiro_semestre,
                'nota_segundo_semestre': a.nota_segundo_semestre,
                'media_final': a.media_final,
                'turma_id': a.turma_id,
                'turma': a.turma.descricao if a.turma else None
            }
            for a in alunos
        ]
        return jsonify(resultado)

    @app.route('/alunos', methods=['POST'])
    def criar_aluno():
        dados = request.get_json()

        turma = Turma.query.get(dados['turma_id'])
        if not turma:
            return jsonify({'erro': 'Turma não encontrada'}), 404

        data_nasc = None
        if 'data_nascimento' in dados:
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

        return jsonify({'mensagem': 'Aluno criado com sucesso', 'id': novo_aluno.id}), 201

    @app.route('/alunos/<int:id>', methods=['PUT'])
    def atualizar_aluno(id):
        aluno = Aluno.query.get_or_404(id)
        dados = request.get_json()

        aluno.nome = dados.get('nome', aluno.nome)
        aluno.idade = dados.get('idade', aluno.idade)

        if 'data_nascimento' in dados:
            aluno.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()

        aluno.nota_primeiro_semestre = dados.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = dados.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        aluno.media_final = dados.get('media_final', aluno.media_final)

        if 'turma_id' in dados:
            turma = Turma.query.get(dados['turma_id'])
            if not turma:
                return jsonify({'erro': 'Turma não encontrada'}), 404
            aluno.turma_id = dados['turma_id']

        db.session.commit()
        return jsonify({'mensagem': 'Aluno atualizado com sucesso'})

    @app.route('/alunos/<int:id>', methods=['DELETE'])
    def deletar_aluno(id):
        aluno = Aluno.query.get_or_404(id)
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno deletado com sucesso'})