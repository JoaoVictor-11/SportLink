import sqlite3

conexao = sqlite3.connect('sportlink.db')
cursor = conexao.cursor()

try:
    cursor.execute("ALTER TABLE usuarios ADD COLUMN foto_perfil TEXT")
    print("✅ Coluna 'foto_perfil' adicionada!")
except:
    print("⚠️ A coluna já existia.")

conexao.commit()
conexao.close()