import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_  # <--- AQUI ESTAVA FALTANDO!
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_do_joao'

# CONFIGURAÇÃO DO BANCO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sportsync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CONFIGURAÇÃO DE UPLOAD
PASTA_UPLOAD = 'static/fotos'
app.config['UPLOAD_FOLDER'] = PASTA_UPLOAD
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(PASTA_UPLOAD, exist_ok=True)

db = SQLAlchemy(app)

# --- MODELOS ---

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    foto_perfil = db.Column(db.String(200), nullable=True)
    grupos_criados = db.relationship('Grupo', backref='dono', lazy=True)

class Grupo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_esporte = db.Column(db.String(100), nullable=False)
    local = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(100), nullable=False)
    dono_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupo.id'))

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

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

    # Lógica de Busca
    termo_busca = request.args.get('q')

    if termo_busca:
        # O '%' significa que pode ter texto antes ou depois
        filtro = f"%{termo_busca}%"
        # Filtra se o Esporte OU o Local contém o texto digitado
        grupos = Grupo.query.filter(
            or_(
                Grupo.nome_esporte.ilike(filtro),
                Grupo.local.ilike(filtro)
            )
        ).all()
    else:
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

# ROTA DO DASHBOARD PESSOAL
@app.route('/meus_jogos')
def meus_jogos():
    if 'user_id' not in session: return redirect('/login')
    
    usuario_id = session['user_id']
    
    # 1. Grupos que EU Criei
    meus_grupos = Grupo.query.filter_by(dono_id=usuario_id).all()
    
    # 2. Grupos que EU Entrei (Inscrições)
    # Aqui fazemos um JOIN: Busque Grupos onde existe uma Inscrição do meu usuário
    # Se der erro aqui, certifique-se que a classe Inscricao e Grupo estão definidas
    grupos_inscritos = db.session.query(Grupo).join(Inscricao).filter(Inscricao.usuario_id == usuario_id).all()
    
    usuario = Usuario.query.get(usuario_id)
    return render_template('meus_jogos.html', criados=meus_grupos, inscritos=grupos_inscritos, usuario_logado=usuario)

# ROTA DE EXCLUSÃO (SÓ O DONO PODE)
@app.route('/excluir_grupo/<int:id_grupo>')
def excluir_grupo(id_grupo):
    if 'user_id' not in session: return redirect('/login')
    
    grupo = Grupo.query.get(id_grupo)
    
    # SEGURANÇA: Verifica se o grupo existe E se quem tá tentando apagar é o dono
    if grupo and grupo.dono_id == session['user_id']:
        # Primeiro removemos as inscrições para não dar erro de chave estrangeira
        Inscricao.query.filter_by(grupo_id=id_grupo).delete()
        
        # Depois removemos o grupo
        db.session.delete(grupo)
        db.session.commit()
        flash("Grupo excluído com sucesso!", "success") # O "success" é pra cor verde
    else:
        flash("Você não tem permissão para excluir este grupo.", "danger") # "danger" é vermelho
        
    return redirect('/meus_jogos')

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
            usuario.foto_perfil = nome_final
        
        db.session.commit()
        session['user_nome'] = usuario.nome
        flash("Perfil atualizado!")

    return render_template('perfil.html', usuario=usuario)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)