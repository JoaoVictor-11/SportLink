import sqlite3

# 1. CONEXÃO
# Cria o arquivo 'sportlink.db' se ele não existir
conexao = sqlite3.connect('sportlink.db')
cursor = conexao.cursor()

print("--- Iniciando Configuração do Banco de Dados ---")

# 2. CRIAÇÃO DAS TABELAS (As gavetas do armário)

# Tabela de Usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT,
    esportes_favoritos TEXT
)
''')
print("Tabela 'usuarios' criada!")

# Tabela de Grupos
# Note o 'FOREIGN KEY': isso diz que o 'dono_id' TEM que ser um ID válido da tabela usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS grupos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_esporte TEXT NOT NULL,
    local TEXT NOT NULL,
    horario TEXT NOT NULL,
    dono_id INTEGER,
    FOREIGN KEY (dono_id) REFERENCES usuarios (id)
)
''')
print("Tabela 'grupos' criada!")

# 3. INSERINDO DADOS DE TESTE (Pra não ficar vazio)

# Vamos inserir o Usuário João (Você)
# Atenção: não passamos o ID, o banco cria sozinho (AUTOINCREMENT)
try:
    cursor.execute('''
    INSERT INTO usuarios (nome, email, telefone, esportes_favoritos)
    VALUES ('João Victor', 'joao@email.com', '1199999-9999', 'Futebol, Vôlei')
    ''')
    print("Usuário João inserido!")
except:
    print("Erro ao inserir usuário (talvez já exista?)")

# Pegar o ID do João que acabamos de criar para usar no grupo
# fetchone() pega o primeiro resultado que encontrar
cursor.execute("SELECT id FROM usuarios WHERE email = 'joao@email.com'")
id_do_joao = cursor.fetchone()[0]

try:
    cursor.execute('''
    INSERT INTO usuarios (nome, email, telefone, esportes_favoritos)
    VALUES ('Neymar Júnior', 'neymar@email.com', '1199999-9999', 'Futebol')
    ''')
    print("Usuário Neymar inserido!")
except:
    print("Erro ao inserir usuário (talvez já exista?)")

# Pegar o ID do Neymar que acabamos de criar para usar no grupo
# fetchone() pega o primeiro resultado que encontrar
cursor.execute("SELECT id FROM usuarios WHERE email = 'neymar@email.com'")
id_do_neymar = cursor.fetchone()[0]

# Vamos inserir um Grupo onde o João é o dono
cursor.execute('''
INSERT INTO grupos (nome_esporte, local, horario, dono_id)
VALUES (?, ?, ?, ?)
''', ('Futebol de Terça', 'Quadra do Centro', 'Terça as 19h', id_do_joao))
print("Grupo de Futebol inserido!")

# Vamos inserir um Grupo onde o Neymar é o dono
cursor.execute('''
INSERT INTO grupos (nome_esporte, local, horario, dono_id)
VALUES (?, ?, ?, ?)
''', ('Futebol de Quarta', 'Vila Belmiro', 'Quarta as 20h', id_do_neymar))
print("Grupo de Futebol inserido!")

# 4. SALVAR E FECHAR
conexao.commit() # O botão de salvar
conexao.close()

print("\n--- Tudo pronto! Banco de dados criado. ---")