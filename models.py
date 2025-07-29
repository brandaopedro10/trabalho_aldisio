from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    cpf = db.Column(db.String(11), nullable =False)
    cidade = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)


    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email,
                'cpf': self.cpf, 'cidade': self.cidade, 'telefone': self.telefone,
                'endereço': self.endereco}
    
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    produtos = db.relationship('Produto', backref='categoria', lazy = True)

    def to_dict(self):
        return {'id': self.id,'nome': self.nome}

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    url_imagem = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {'id': self.id,'nome': self.nome, 'descricao': self.descricao, 'preço': self.preco, 'categoria ID': self.categoria_id, 'URL imagem': self.url_imagem}

