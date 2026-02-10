import sqlite3

conexao = sqlite3.connect('sportlink.db')
cursor = conexao.cursor()

print("--- Atualizando Banco de Dados ---")

# Criando a tabela que liga usuários a grupos
cursor.execute('''
CREATE TABLE IF NOT EXISTS inscricoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    grupo_id INTEGER,
    data_inscricao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (grupo_id) REFERENCES grupos (id)
)
''')

print("✅ Tabela 'inscricoes' criada com sucesso!")
conexao.commit()
conexao.close()