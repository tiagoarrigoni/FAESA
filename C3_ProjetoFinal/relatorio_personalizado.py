from dados import nomes_jogadores, notas_mortal_kombat, notas_forza5, notas_dota, notas_csgo, largura_coluna

# Função para exibir o relatório personalizado em formato de tabela
def relatorioPersonalizado():
    if not nomes_jogadores:
        print("\nNenhum jogador cadastrado. Inicie o campeonato primeiro.")
        return
    
    # Exibe a lista de jogadores para seleção
    print("\nRelatório Personalizado:\n")
    print("Escolha o jogador:")
    for i, jogador in enumerate(nomes_jogadores, start=1):
        print(f"{i}. {jogador}")
    
    # Solicita a escolha do jogador
    opcao_jogador = int(input("\nDigite o número do jogador: ")) - 1
    
    if 0 <= opcao_jogador < len(nomes_jogadores):
        jogador_selecionado = nomes_jogadores[opcao_jogador]
        
        # Dados das pontuações do jogador selecionado
        pontuacoes = [
            ["Mortal Kombat", notas_mortal_kombat[opcao_jogador][0] if len(notas_mortal_kombat) > opcao_jogador else "N/A"],
            ["Forza5", notas_forza5[opcao_jogador][0] if len(notas_forza5) > opcao_jogador else "N/A"],
            ["Dota", notas_dota[opcao_jogador][0] if len(notas_dota) > opcao_jogador else "N/A"],
            ["CSGO", notas_csgo[opcao_jogador][0] if len(notas_csgo) > opcao_jogador else "N/A"]
        ]

        # Função para formatação das notas
        def formatar_pontuacao(pontuacao):
            if isinstance(pontuacao, int):
                return f"{pontuacao:,.0f}"  # Formatação com separadores de milhar
            return pontuacao  # Para "N/A"

        # Tabela formatada manualmente
        print(f"\nPontuações de {jogador_selecionado}:\n")
        print(f"+{'-'*16}{'-'*15}+")
        print(f"| {'Jogo':<16} | {'Pontuação':<10} |")
        print(f"+{'-'*16}{'-'*15}+")
        for jogo, nota in pontuacoes:
            print(f"| {jogo:<16} | {formatar_pontuacao(nota):<10} |")
        print(f"+{'-'*16}{'-'*15}+")
    else:
        print("\nNúmero de jogador inválido!")
