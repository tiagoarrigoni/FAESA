from dados import nomes_jogadores, notas_mortal_kombat, notas_forza5, notas_dota, notas_csgo

def armazenarNotas(matriz, nome_jogo):
    # Limpa a matriz de notas antes de adicionar as novas pontuações
    matriz.clear()
    
    print(f"\nInserindo pontuações para {nome_jogo}:")
    for i in range(len(nomes_jogadores)):
        # Solicita a pontuação do jogador
        nota = int(input(f"Informe a pontuação de {nomes_jogadores[i]}: "))
        
        # Adiciona a pontuação na matriz. Cada jogador tem uma lista de notas.
        matriz.append([nota])  # Aqui, o nota é armazenada em uma lista dentro da matriz.
    
    print(f"Pontuações para {nome_jogo} registradas com sucesso!")

def iniciarCampeonato():
    global nomes_jogadores
    
    # Solicita a quantidade de jogadores
    num_jogadores = int(input("Informe a quantidade de jogadores: "))
    
    # Coleta o nome dos jogadores
    nomes_jogadores.clear()  # Limpa a lista de jogadores antes de adicionar novos
    for i in range(num_jogadores):
        nome = input(f"Nome do jogador {i + 1}: ")
        nomes_jogadores.append(nome)
    
    # Loop para permitir o cadastro em múltiplos jogos
    while True:
        # Submenu de jogos
        print("\nSelecione o jogo para inserir as pontuações:")
        print("1. Mortal Kombat")
        print("2. Forza5")
        print("3. Dota")
        print("4. CSGO")
        
        jogo_opcao = input("\nEscolha o jogo: ")
        
        # Armazena as notas de acordo com o jogo escolhido
        if jogo_opcao == "1":
            armazenarNotas(notas_mortal_kombat, "Mortal Kombat")
        elif jogo_opcao == "2":
            armazenarNotas(notas_forza5, "Forza5")
        elif jogo_opcao == "3":
            armazenarNotas(notas_dota, "Dota")
        elif jogo_opcao == "4":
            armazenarNotas(notas_csgo, "CSGO")
        else:
            print("Opção de jogo inválida!")
        
        # Pergunta ao usuário se deseja cadastrar mais jogos
        continuar = input("\nDeseja cadastrar mais jogos? (S/N): ").strip().upper()
        if continuar != 'S':
            break  # Sai do loop e volta ao menu principal
