from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

turma_alunos = db.Table('turma_alunos',
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True),
    db.Column('aluno_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
)

turma_materias = db.Table('turma_materias',
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True),
    db.Column('materia_id', db.Integer, db.ForeignKey('materias.id'), primary_key=True)
)


class Usuario(db.Model):
  
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    ra = db.Column(db.String(20), unique=True, nullable=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False) 

    turmas = db.relationship('Turma', secondary=turma_alunos, back_populates='alunos')

    def set_senha(self, senha):
       
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
    
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.role})>'

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)

    alunos = db.relationship('Usuario', secondary=turma_alunos, back_populates='turmas')
    
    materias = db.relationship('Materia', secondary=turma_materias, back_populates='turmas')

    def __repr__(self):
        return f'<Turma {self.nome}>'
    
class Materia(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    professor = db.relationship('Usuario', backref='materias_lecionadas')

   
    turmas = db.relationship('Turma', secondary=turma_materias, back_populates='materias')

class Inscricao(db.Model):
    __tablename__ = 'inscricoes'
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), primary_key=True)


    aluno = db.relationship('Usuario', backref=db.backref('inscricoes', cascade="all, delete-orphan"))
    materia = db.relationship('Materia', backref=db.backref('inscricoes', cascade="all, delete-orphan"))

class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_entrega = db.Column(db.DateTime, nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    
    materia = db.relationship('Materia', backref='atividades')

class Entrega(db.Model):
    __tablename__ = 'entregas'
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text) 
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    nota = db.Column(db.Float)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)

    aluno = db.relationship('Usuario', backref='entregas')
    atividade = db.relationship('Atividade', backref='entregas')

class Presenca(db.Model):
    __tablename__ = 'presencas'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, default=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)

    aluno = db.relationship('Usuario', backref='presencas')
    materia = db.relationship('Materia', backref='presencas')