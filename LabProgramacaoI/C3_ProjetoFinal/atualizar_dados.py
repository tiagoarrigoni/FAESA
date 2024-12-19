from dados import nomes_jogadores, notas_mortal_kombat, notas_forza5, notas_dota, notas_csgo
from recompensas import calcularRecompensas  # Importar a nova função

# Atualizar dados e recompensas
def atualizarDados():
    if not nomes_jogadores:
        print("\nNenhum jogador cadastrado. Não é possível atualizar dados.")
        return
    
    # Exibir lista de jogadores com números e nomes
    print("\nJogadores cadastrados:")
    for i, nome in enumerate(nomes_jogadores, 1):
        print(f"{i}. {nome}")
    
    # Menu de opções de atualização
    print("\nAtualizar Dados de Jogadores:")
    print("1. Alterar nome de jogador")
    print("2. Remover jogador")
    print("3. Alterar pontuação de jogo")
    opcao = input("\nEscolha a opção: ")
    
    if opcao == "1":
        # Alterar nome de jogador
        jogador_index = int(input("\nDigite o número do jogador a ser alterado: ")) - 1
        if 0 <= jogador_index < len(nomes_jogadores):
            novo_nome = input("Digite o novo nome: ")
            nomes_jogadores[jogador_index] = novo_nome
            print(f"Nome alterado para: {novo_nome}")
        else:
            print("Jogador não encontrado!")
    
    elif opcao == "2":
        # Remover jogador
        jogador_index = int(input("\nDigite o número do jogador a ser removido: ")) - 1
        if 0 <= jogador_index < len(nomes_jogadores):
            del nomes_jogadores[jogador_index]
            del notas_mortal_kombat[jogador_index]
            del notas_forza5[jogador_index]
            del notas_dota[jogador_index]
            del notas_csgo[jogador_index]
            print("Jogador removido com sucesso!")
        else:
            print("Jogador não encontrado!")
    
    elif opcao == "3":
        # Alterar pontuação de algum jogo
        jogador_index = int(input("\nDigite o número do jogador a ser alterado: ")) - 1
        if 0 <= jogador_index < len(nomes_jogadores):
            jogo_opcao = input("Digite o nome do jogo (Mortal Kombat, Forza5, Dota, CSGO): ").strip().lower()
            nova_pontuacao = int(input("Digite a nova pontuação: "))
            
            if jogo_opcao == "mortal kombat":
                notas_mortal_kombat[jogador_index][0] = nova_pontuacao
            elif jogo_opcao == "forza5":
                notas_forza5[jogador_index][0] = nova_pontuacao
            elif jogo_opcao == "dota":
                notas_dota[jogador_index][0] = nova_pontuacao
            elif jogo_opcao == "csgo":
                notas_csgo[jogador_index][0] = nova_pontuacao
            else:
                print("Jogo inválido!")
                return
            
            print("Pontuação atualizada!")
            # Recalcula as recompensas
            recompensas = calcularRecompensas()
            print("Recompensas recalculadas!")
        else:
            print("Jogador não encontrado!")
