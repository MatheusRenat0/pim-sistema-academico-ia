from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class Usuario(db.Model):
  
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    ra = db.Column(db.String(20), unique=True, nullable=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False) 

    def set_senha(self, senha):
       
        self.senha_hash = generate_password_hash(senha)
    
    def check_senha(self, senha):
    
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.role})>'