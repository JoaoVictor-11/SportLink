import sqlite3

# 1. Conectar no mesmo banco que criamos antes
conexao = sqlite3.connect('sportlink.db')
cursor = conexao.cursor()

print("\n=== LISTA DE USUÁRIOS ===")
# O comando SELECT * pega TODAS as colunas
cursor.execute("SELECT id, nome, email FROM usuarios")
usuarios = cursor.fetchall() # fetchall = "pegue tudo e traga pra mim"

for u in usuarios:
    # u[0] é o ID, u[1] é o Nome...
    print(f"ID: {u[0]} | Nome: {u[1]} | Email: {u[2]}")

print("\n=== LISTA DE GRUPOS (COM O NOME DO DONO) ===")

# AQUI ESTÁ A MÁGICA DE ARQUITETO (O JOIN)
# Não queremos ver "Dono_ID: 2", queremos ver "Dono: Maria"
# O INNER JOIN serve para juntar as duas tabelas onde os IDs batem
sql_avancado = '''
SELECT grupos.nome_esporte, grupos.local, grupos.horario, usuarios.nome
FROM grupos
INNER JOIN usuarios ON grupos.dono_id = usuarios.id
'''

cursor.execute(sql_avancado)
grupos = cursor.fetchall()

for g in grupos:
    print(f"Esporte: {g[0]}")
    print(f"Local: {g[1]} | Horário: {g[2]}")
    print(f"Dono do Grupo: {g[3]}") # Aqui vai aparecer o nome da pessoa, não o número!
    print("-" * 30)

conexao.close()