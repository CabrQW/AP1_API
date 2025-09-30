import os
from flask import Flask
from config import Config
from models import db 

def criar_app():

    app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
    

    app.config.from_object(Config)
    

    db.init_app(app)

    with app.app_context():

        from models.aluno import Aluno
        from models.turma import Turma
        from models.professor import Professor

        db.create_all()

        from controllers.aluno_controller import registrar_rotas_alunos
        from controllers.professor_controller import registrar_rotas_professor
        from controllers.turma_controller import registrar_rotas_turmas

        registrar_rotas_alunos(app)
        registrar_rotas_professor(app)
        registrar_rotas_turmas(app)

        print("App iniciado e todas as tabelas criadas com sucesso!")

    return app


if __name__ == "__main__":
    # Cria o app e roda o servidor
    app = criar_app()
    app.run(debug=True)