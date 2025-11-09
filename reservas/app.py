from flask import Flask
from flasgger import Swagger
from models import db
from controllers.reserva_controller import reserva_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'API de Reservas',
        'uiversion': 3
    }

    db.init_app(app)
    Swagger(app)

    app.register_blueprint(reserva_bp, url_prefix='/api/reservas')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
