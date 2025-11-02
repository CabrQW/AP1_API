from app import db

class Notas(db.Model):
    _tablename_ = 'notas'

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)

    aluno = db.relationship('Aluno', backref=db.backref('notas', lazy=True))
    atividade = db.relationship('Atividades', backref=db.backref('notas', lazy=True))