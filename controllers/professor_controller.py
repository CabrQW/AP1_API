from flask import request, jsonify
from app import db
from models.professor import Professor

def registrar_rotas_professor(app):

    @app.route('/professores', methods=['GET'])
    def listar_professores():
        professores = Professor.query.all()
        resultado = [{'id': p.id, 
                      'nome': p.nome, 
                      'idade': p.idade, 
                      'materia': p.materia, 
                      'observacao': p.observacao, 
                      'turmas': [t.nome for t in p.turmas]
                      } 
                      for p in professores
        ]
        return jsonify(resultado)
    @app.route('/professores', methods=['POST'])
    def criar_professor():
        dados = request.get_json()
        novo = Professor(
            nome = dados['nome'],
            idade = dados['idade'],
            materia = dados['materia'],
            observacao = dados['observacao']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Professor criado', 'id': novo.id}), 201
    @app.route('/professores/<int:id>', methods=['PUT'])
    def atualizar_professor(id):
        prof = Professor.query.get_or_404(id)
        dados = request.get_json()
        prof.nome = dados.get('nome', prof.nome)
        prof.idade = dados.get('idade', prof.idade)
        prof.materia = dados.get('materia', prof.materia)
        prof.observacao = dados.get('observacao', prof.observacao)
        db.session.commit()
        return jsonify({'mensagem': 'Professor atualizado.'})
    @app.route('/professores/<int:id>', methods=['DELETE'])
    def deletar_professor(id):
        prof = Professor.query.get_or_404(id)
        db.session.delete(prof)
        db.session.commit()
        return jsonify({'mensagem': 'Professor deletado.'})