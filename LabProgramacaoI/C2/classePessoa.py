class Pessoa:
    def __init__(self, nome, idade, profissao):
        try:
            if not isinstance(nome, str):
                raise TypeError("O nome deve ser uma string")
            if not isinstance(idade, int) or idade < 0:
                raise ValueError("A idade deve ser um numero inteiro positivo")
            if not isinstance(profissao, str):
                raise TypeError("A profissao deve ser uma string")
        except (TypeError, ValueError) as e:
            print("Erro ao criar pessoa:", e)
            raise
        else:
            self.nome = nome
            self.idade = idade
            self.profissao = profissao

    def cumprimentar(self):
        return f"Ola, meu nome e {self.nome}!"

    def aniversario(self):
        try:
            self.idade += 1
        except TypeError:
            print("Erro: idade nao e um numero")
        return f"Agora tenho {self.idade} anos!"

# Casos de teste
try:
    p1 = Pessoa("Tiago", 30, "Professor")
    print(p1.cumprimentar())
    print(p1.aniversario())
except Exception as e:
    print("Erro inesperado:", e)

# Casos com erro
try:
    p2 = Pessoa(123, "trinta", 10)  # Erros de tipo e valor
except Exception as e:
    print("Excecao capturada:", e)
