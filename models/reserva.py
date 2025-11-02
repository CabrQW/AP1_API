from app import db

class Reservas(db.Model):
    _tablename_ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)

    turma = db.relationship('Turma', backref=db.backref('reservas', lazy=True))