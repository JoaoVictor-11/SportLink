import sqlite3

conexao = sqlite3.connect('sportlink.db')
cursor = conexao.cursor()

try:
    # O comando ALTER TABLE adiciona uma coluna nova numa tabela existente
    cursor.execute("ALTER TABLE usuarios ADD COLUMN senha TEXT")
    print("✅ Coluna 'senha' adicionada com sucesso!")
except:
    print("⚠️ A coluna senha provavelmente já existe.")

conexao.commit()
conexao.close()