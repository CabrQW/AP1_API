from app import db

class Atividades(db.Model):
    _tablename_ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100), nullable=True)
    peso_porcento = db.Column(db.Float, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)

    turma = db.relationship('Turma', backref=db.backref('atividades', lazy=True))
    professor = db.relationship('Professor', backref=db.backref('atividades', lazy=True))