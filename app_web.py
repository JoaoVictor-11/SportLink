import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_do_joao'

# CONFIGURAÇÃO DO BANCO (SQLALCHEMY)
# Note que agora configuramos tudo no objeto 'app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportlink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CONFIGURAÇÃO DE UPLOAD
PASTA_UPLOAD = 'static/fotos'
app.config['UPLOAD_FOLDER'] = PASTA_UPLOAD
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(PASTA_UPLOAD, exist_ok=True)

# INICIALIZANDO O ORM
db = SQLAlchemy(app)

# --- MODELOS (As Tabelas viram Classes) ---

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    foto_perfil = db.Column(db.String(200), nullable=True)
    
    # Relacionamento: Um usuário é dono de vários grupos
    # O 'backref' cria uma propriedade 'dono' mágica dentro da classe Grupo
    grupos_criados = db.relationship('Grupo', backref='dono', lazy=True)

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_esporte = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(100), nullable=False)
    
    # Chave Estrangeira ligando ao Usuario
    dono_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Tabela de Associação (Inscrições)
class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'))

# --- FUNÇÃO AUXILIAR ---
def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

# --- CRIAÇÃO DO BANCO ---
# Isso substitui aqueles scripts 'setup_banco.py'
with app.app_context():
    db.create_all()

# --- ROTAS ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/feed')
    return render_template('landing.html')

@app.route('/feed')
def feed():
    if 'user_id' not in session:
        return redirect('/login')

    # OLHA A MÁGICA DO ORM AQUI:
    # Em vez de SELECT com JOIN, pegamos os objetos.
    # O HTML vai acessar o nome do dono via 'grupo.dono.nome' automaticamente!
    grupos = Grupo.query.all()
    
    usuario = Usuario.query.get(session['user_id'])
    
    return render_template('feed.html', grupos=grupos, usuario_logado=usuario)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)

        # JEITO NOVO DE SALVAR
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect('/login')
        except:
            return "Erro: Email já existe."
            
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # JEITO NOVO DE BUSCAR
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            session['user_nome'] = usuario.nome
            return redirect('/feed')
        else:
            flash('Email ou senha incorretos')
            
    return render_template('login.html')

@app.route('/criar', methods=['GET', 'POST'])
def criar_grupo():
    if 'user_id' not in session: return redirect('/login')

    if request.method == 'POST':
        # JEITO NOVO DE CRIAR GRUPO
        novo_grupo = Grupo(
            nome_esporte=request.form['esporte'],
            local=request.form['local'],
            horario=request.form['horario'],
            dono_id=session['user_id']
        )
        db.session.add(novo_grupo)
        db.session.commit()
        return redirect('/feed')

    return render_template('criar_grupo.html')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session: return redirect('/login')

    usuario = Usuario.query.get(session['user_id'])

    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        
        arquivo = request.files.get('foto')
        if arquivo and arquivo.filename != '' and arquivo_permitido(arquivo.filename):
            nome_seguro = secure_filename(arquivo.filename)
            extensao = nome_seguro.rsplit('.', 1)[1].lower()
            nome_final = f"perfil_{usuario.id}.{extensao}"
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_final))
            usuario.foto_perfil = nome_final # Atualiza o objeto
        
        db.session.commit() # O SQLalchemy detecta as mudanças e salva
        session['user_nome'] = usuario.nome
        flash("Perfil atualizado!")

    return render_template('perfil.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)