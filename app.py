import sqlite3

def conectar():
    return sqlite3.connect('sportlink.db')

def main():
    conexao = conectar()
    cursor = conexao.cursor()

    print("\nBem-vindo ao SportLink (Terminal Version) ⚽🏐")

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Cadastrar Novo Usuário")
        print("2. Criar Novo Grupo")
        print("3. Listar Grupos Disponíveis")
        print("4. Listar TODOS Usuários (Para ver IDs)")
        print("5. Entrar em um Grupo")    # Renumerado
        print("6. Ver Jogadores do Grupo") # Renumerado
        print("7. Sair")                   # Renumerado
        
        opcao = input("Escolha uma opção: ")

        # 1. CADASTRAR USUÁRIO
        if opcao == '1':
            nome = input("Nome do Usuário: ")
            email = input("Email: ")
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            conexao.commit()
            print(f"✅ Sucesso! Usuário '{nome}' cadastrado.")
            print(f"ℹ️  O ID deste novo usuário é: {cursor.lastrowid}") 

        # 2. CRIAR GRUPO
        elif opcao == '2':
            id_dono = input("Digite o ID do Usuário dono do grupo: ")
            esporte = input("Qual o esporte? ")
            local = input("Onde será? ")
            horario = input("Qual horário? ")
            
            try:
                cursor.execute('''
                INSERT INTO grupos (nome_esporte, local, horario, dono_id)
                VALUES (?, ?, ?, ?)
                ''', (esporte, local, horario, id_dono))
                conexao.commit()
                print(f"✅ Grupo de {esporte} criado!")
            except:
                print("❌ Erro ao criar grupo. Verifique se o ID do dono existe.")

        # 3. LISTAR GRUPOS
        elif opcao == '3':
            print("\n--- GRUPOS ---")
            cursor.execute('''
            SELECT grupos.id, grupos.nome_esporte, usuarios.nome 
            FROM grupos JOIN usuarios ON grupos.dono_id = usuarios.id
            ''')
            grupos = cursor.fetchall()
            for g in grupos:
                print(f"Grupo #{g[0]}: {g[1]} (Dono: {g[2]})")

        # 4. LISTAR USUÁRIOS
        elif opcao == '4':
            print("\n--- LISTA DE USUÁRIOS ---")
            cursor.execute("SELECT id, nome FROM usuarios")
            usuarios = cursor.fetchall()
            for u in usuarios:
                print(f"ID: {u[0]} | Nome: {u[1]}")
            print("-------------------------")
            
        # 5. ENTRAR EM UM GRUPO (Corrigido para 5)
        elif opcao == '5':
            id_usuario = input("Seu ID de usuário: ")
            id_grupo = input("ID do grupo que quer entrar: ")

            try:
                # Verifica se já não está inscrito
                cursor.execute("SELECT * FROM inscricoes WHERE usuario_id = ? AND grupo_id = ?", (id_usuario, id_grupo))
                if cursor.fetchone():
                    print("⚠️  Você já está nesse grupo!")
                else:
                    cursor.execute("INSERT INTO inscricoes (usuario_id, grupo_id) VALUES (?, ?)", (id_usuario, id_grupo))
                    conexao.commit()
                    print("✅ Parabéns! Você entrou no grupo.")
            except Exception as e:
                print(f"❌ Erro: {e}")

        # 6. VER MEMBROS DE UM GRUPO (Corrigido para 6)
        elif opcao == '6':
            id_grupo = input("Digite o ID do grupo para ver quem joga lá: ")
            
            sql = '''
            SELECT usuarios.nome 
            FROM inscricoes
            JOIN usuarios ON inscricoes.usuario_id = usuarios.id
            WHERE inscricoes.grupo_id = ?
            '''
            cursor.execute(sql, (id_grupo,))
            membros = cursor.fetchall()
            
            print(f"\n--- Jogadores do Grupo {id_grupo} ---")
            if not membros:
                print("Ninguém entrou nesse grupo ainda.")
            else:
                for m in membros:
                    print(f"⚽ {m[0]}")

        # 7. SAIR
        elif opcao == '7':
            print("Saindo... Até a próxima!")
            break
        
        else:
            print("Opção inválida!")

    conexao.close()

if __name__ == "__main__":
    main()