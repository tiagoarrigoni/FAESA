class Veiculo:
    def __init__(self, marca, modelo, ano):
        try:
            if not isinstance(marca, str) or not isinstance(modelo, str):
                raise TypeError("Marca e modelo devem ser strings")
            if not isinstance(ano, int) or ano < 1886:
                raise ValueError("Ano invalido para um veiculo")
        except (TypeError, ValueError) as e:
            print("Erro ao criar veiculo:", e)
            raise
        else:
            self.marca = marca
            self.modelo = modelo
            self.ano = ano

    def descricao(self):
        return f"{self.marca} {self.modelo} ({self.ano})"


class Carro(Veiculo):
    def __init__(self, marca, modelo, ano, numero_portas):
        super().__init__(marca, modelo, ano)
        try:
            if not isinstance(numero_portas, int) or numero_portas not in [2, 4]:
                raise ValueError("Numero de portas deve ser 2 ou 4")
        except ValueError as e:
            print("Erro ao criar carro:", e)
            raise
        else:
            self.numero_portas = numero_portas


class Moto(Veiculo):
    def __init__(self, marca, modelo, ano, cilindradas):
        super().__init__(marca, modelo, ano)
        try:
            if not isinstance(cilindradas, int) or cilindradas <= 0:
                raise ValueError("Cilindradas devem ser maiores que zero")
        except ValueError as e:
            print("Erro ao criar moto:", e)
            raise
        else:
            self.cilindradas = cilindradas


# Casos de teste
try:
    carro = Carro("Toyota", "Corolla", 2020, 4)
    moto = Moto("Honda", "CB500", 2021, 500)
    print(carro.descricao())
    print(moto.descricao())
except Exception as e:
    print("Erro:", e)

# Casos com erro
try:
    carro2 = Carro("Fiat", "Uno", 1980, 3)
except Exception as e:
    print("Excecao capturada:", e)
