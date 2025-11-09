from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Importa apenas o db aqui
from models import db

app = Flask(__name__)

# Configuração do banco SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {
    'title': 'API de Atividades',
    'uiversion': 3
}

db.init_app(app)
swagger = Swagger(app)

# Importa os blueprints *depois* de inicializar o app e db
from controllers.atividade_controller import atividade_bp
from controllers.nota_controller import nota_bp

app.register_blueprint(atividade_bp, url_prefix="/api/atividades")
app.register_blueprint(nota_bp, url_prefix="/api/notas")

# Cria tabelas
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"mensagem": "API de Atividades e Notas está rodando com sucesso 🚀"}

if __name__ == "__main__":
    app.run(debug=True)
