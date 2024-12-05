from dados import nomes_jogadores, notas_mortal_kombat, notas_forza5, notas_dota, notas_csgo


# Função para calcular as recompensas detalhadas
def calcularRecompensas():
    recompensas = []
    
    for i, jogador in enumerate(nomes_jogadores):
        # Calcula as recompensas por jogo
        recompensa_mortal_kombat = notas_mortal_kombat[i][0] * 15 if len(notas_mortal_kombat) > i else 0
        recompensa_forza5 = notas_forza5[i][0] * 25 if len(notas_forza5) > i else 0
        recompensa_dota = notas_dota[i][0] * 100 if len(notas_dota) > i else 0
        recompensa_csgo = notas_csgo[i][0] * 200 if len(notas_csgo) > i else 0
        
        # Soma total
        total_recompensa = recompensa_mortal_kombat + recompensa_forza5 + recompensa_dota + recompensa_csgo
        
        # Adiciona ao array de recompensas
        recompensas.append({
            "mortal_kombat": recompensa_mortal_kombat,
            "forza5": recompensa_forza5,
            "dota": recompensa_dota,
            "csgo": recompensa_csgo,
            "total": total_recompensa
        })
    
    return recompensas

# Função para exibir as recompensas detalhadas
def mostrarRecompensas():
    if not nomes_jogadores:
        print("\nNenhum jogador cadastrado. Inicie o campeonato primeiro.")
        return
    
    recompensas = calcularRecompensas()

    # Cabeçalhos da tabela
    print("\n=====================================================================================================================")
    print("|*|                                             TABELA DE RECOMPENSAS                                             |*|")
    print("=====================================================================================================================")
    print("="*117)
    print(f"| {'Jogador':<15} | {'Mortal Kombat (R$)':<20} | {'Forza 5 (R$)':<20} | {'Dota (R$)':<15} | {'CS:GO (R$)':<14} | {'Total (R$)':<14} |")
    print("="*117)
    
    maior_recompensa = 0
    vencedor = ""

    # Itera sobre cada jogador e exibe suas recompensas detalhadas
    for i, jogador in enumerate(nomes_jogadores):
        recompensa = recompensas[i]
        
        print(f"| {jogador:<15} | R$ {recompensa['mortal_kombat']:17,.2f} | R$ {recompensa['forza5']:17,.2f} | R$ {recompensa['dota']:12,.2f} | R$ {recompensa['csgo']:11,.2f} | R$ {recompensa['total']:11,.2f} |")
        
        # Verifica se o jogador tem a maior recompensa total
        if recompensa['total'] > maior_recompensa:
            maior_recompensa = recompensa['total']
            vencedor = jogador
    
    # Rodapé da tabela
    print("="*117)