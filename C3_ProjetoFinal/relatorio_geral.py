from dados import nomes_jogadores, notas_mortal_kombat, notas_forza5, notas_dota, notas_csgo, largura_coluna, largura_final

# Função para exibir o relatório geral em formato de tabela
def relatorioGeral():
    if not nomes_jogadores:
        print("\nNenhum jogador cadastrado.")
        return
    
    # Cabeçalhos da tabela
    print("\n===========================================================================================")
    print("|*|                                TABELA DE PONTUAÇÕES                                 |*|")
    print("===========================================================================================")
    print(f"+{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_final}+")
    print(f"| {'Jogador':<{largura_coluna}} | {'Mortal Kombat':<{largura_coluna}} | {'Forza5':<{largura_coluna}} | {'Dota':<{largura_coluna}} | {'CSGO':<{largura_coluna}} |")
    print(f"+{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_final}+")
    
    # Itera sobre cada jogador e exibe suas pontuações
    for i, jogador in enumerate(nomes_jogadores):
        mortal_kombat = notas_mortal_kombat[i][0] if len(notas_mortal_kombat) > i else "N/A"
        forza5 = notas_forza5[i][0] if len(notas_forza5) > i else "N/A"
        dota = notas_dota[i][0] if len(notas_dota) > i else "N/A"
        csgo = notas_csgo[i][0] if len(notas_csgo) > i else "N/A"
        
        # Linha da tabela com os dados do jogador
        print(f"| {jogador:<{largura_coluna}} | {mortal_kombat:<{largura_coluna}} | {forza5:<{largura_coluna}} | {dota:<{largura_coluna}} | {csgo:<{largura_coluna}} |")

    # Rodapé da tabela (com o sinal de "+" no final)
    print(f"+{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_coluna}{'-'*largura_final}+")
