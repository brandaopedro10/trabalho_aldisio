from flask import Flask, request,jsonify
from flask_jwt_extended import(JWTManager, jwt_required,get_jwt_identity, create_access_token)
from models import db, Usuario, Produto, Categoria
from config import Config
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

with app.app_context():
    db.create_all()
 
@app.route("/usuarios", methods=['POST'])
def criar_usuário():
    dados = request.json
    if Usuario.query.filter_by(email = dados['email']).first():
        return jsonify({'erro: Email ja cadastrado'}),409
    usuario = Usuario(nome = dados['nome'], email = dados['email'])
    usuario.set_senha(dados['senha'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict()),201

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    if usuario and usuario.verificar_senha(dados['senha']):
        token = create_access_token(identity=str(usuario.id))
        return jsonify(access_token=token)
    return jsonify({"erro": "Credenciais inválidas"}), 401

@app.route('/produto', methods=['POST'])
def criar_produto():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')
    categoria_id = request.form.get('categoria_id')
    arquivo_imagem = request.files.get('imagem')

    try:
        preco_float = float(preco)
    except (ValueError, TypeError):
        return jsonify({'erro': 'preço invalido'}), 400
    
    url_imagem_db = None
    if arquivo_imagem and allowed_file(arquivo_imagem.filename):
        filename = secure_filename(arquivo_imagem.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 
        caminho_salvar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo_imagem.save(caminho_salvar)
        url_imagem_db = f'/static/imagens/{filename}'
    else:
        return jsonify({'erro': 'Upload de imagem inválido ou tipo de arquivo não permitido.'}), 400
    
    try:
        categoria_id_int = int(categoria_id)
    except ValueError:
        return jsonify({'erro': 'ID da categoria inválido. Deve ser um número inteiro.'}), 400

    categoria_obj = Categoria.query.get(categoria_id_int)
    if not categoria_obj:
        return jsonify({'erro': f'Categoria com ID {categoria_id} não encontrada.'}), 404


    novo_produto = Produto(
        nome=nome,
        descricao=descricao,
        preco=preco_float,
        categoria= categoria_obj,
        url_imagem=url_imagem_db
    )

    db.session.add(novo_produto)
    db.session.commit()


    return jsonify({
        'mensagem': 'produto criado com sucesso',
        'id': novo_produto.id,
        'nome': novo_produto.nome,
        'descrição': novo_produto.descricao,
        'preço': novo_produto.preco,
        'categoria': novo_produto.categoria.to_dict(),
        'url_imagem': novo_produto.url_imagem
    }), 201

@app.route('/produto', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@app.route('/categorias', methods=['POST'])
def criar_categoria():
    dados = request.json
    categoria = Categoria(nome = dados['nome'])
    db.session.add(categoria)
    db.session.commit()
    return jsonify(categoria.to_dict()),201

@app.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([categoria.to_dict() for categoria in categorias]),200

@app.route('/produtos/categoria/<int:categoria_id>', methods=['GET'])
def get_produtos_por_categoria(categoria_id):
    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        return jsonify({"mensagem": "Categoria não encontrada"}), 404

    produtos = Produto.query.filter_by(categoria_id=categoria_id).all()
    return jsonify([produto.to_dict() for produto in produtos])

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_detalhes_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if produto:
        return jsonify(produto.to_dict())
    return jsonify({"mensagem": "Produto não encontrado"}), 404



if __name__ == '__main__':
    app.run(debug=True, port=5055)



