from iniciar_campeonato import iniciarCampeonato
from relatorio_personalizado import relatorioPersonalizado
from relatorio_geral import relatorioGeral
from atualizar_dados import atualizarDados
from recompensas import mostrarRecompensas  

# Variável para verificar se o campeonato foi iniciado
campeonato_iniciado = False

# Função para exibir o menu principal
def menu():
    print("\n+------------------------------------------------------+")
    
    # Mostrar informações apenas se o campeonato não estiver iniciado
    if not campeonato_iniciado:
        print("+      PROJETO FINAL LABORATÓRIO DE PROGRAMAÇÃO 1      +")
        print("+------------------------------------------------------+")
        print("+ ALUNO: TIAGO ARRIGONI                                +")
        print("+------------------------------------------------------+")
        print("+ PROFESSORA: RENATA LARANJA                           +")
        print("+------------------------------------------------------+")
        print("+ CURSO: ANÁLISE E DESENVOLVIMENTO DE SISTEMAS         +")
        print("-------------------------------------------------------+")

        print("\n========================================================")
        print("|*|            CAMPEONATO DE JOGOS DIGITAIS          |*|")
        print("========================================================")
    else:
        print("+               CAMPEONATO (Em Andamento)              +")
        print("+------------------------------------------------------+")
    

    
    if not campeonato_iniciado:  # Se o campeonato não foi iniciado
        print("1. Iniciar Campeonato")
    else:  # Se o campeonato já foi iniciado
        print("-1. Resetar Campeonato")
    
    print("2. Relatório Pontuações")
    print("3. Relatório Recompensas")
    print("4. Relatório Geral")
    print("5. Atualizar Dados")
    print("6. Sair")
    return input("\nEscolha uma opção: ")

# Menu Principal - Loop de Opções disponíveis
while True:
    opcao = menu()
    
    if opcao == "1" and not campeonato_iniciado:  # Inicia o campeonato se ainda não iniciado
        iniciarCampeonato()
        campeonato_iniciado = True  # Atualiza o status para indicar que o campeonato foi iniciado
    elif opcao == "-1" and campeonato_iniciado:  # Reseta o campeonato
        print("\nCampeonato resetado com sucesso!")
        campeonato_iniciado = False  # Atualiza o status para indicar que o campeonato foi resetado
    elif opcao == "2":
        relatorioPersonalizado()
    elif opcao == "3":
        mostrarRecompensas()
    elif opcao == "4":
        relatorioGeral()
        mostrarRecompensas() 
    elif opcao == "5":
        atualizarDados()
    elif opcao == "6":
        print("Encerrando o programa...")
        break
    else:
        print("Opção inválida. Tente novamente!")
