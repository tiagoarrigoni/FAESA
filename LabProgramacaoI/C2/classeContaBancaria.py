class ContaBancaria:
    def __init__(self, titular, numero_conta):
        self.titular = titular
        self.numero_conta = numero_conta
        self.saldo = 0.0

    def depositar(self, valor):
        try:
            if not isinstance(valor, (int, float)):
                raise TypeError("O valor deve ser numerico")
            if valor <= 0:
                raise ValueError("O valor do deposito deve ser positivo")
            self.saldo += valor
        except (TypeError, ValueError) as e:
            print("Erro ao depositar:", e)

    def sacar(self, valor):
        try:
            if not isinstance(valor, (int, float)):
                raise TypeError("O valor do saque deve ser numerico")
            if valor > self.saldo:
                raise ValueError("Saldo insuficiente para o saque")
            self.saldo -= valor
        except (ValueError, TypeError) as e:
            print("Erro ao sacar:", e)

    def consultar_saldo(self):
        try:
            return f"Saldo atual: R$ {self.saldo:.2f}"
        except Exception:
            print("Erro ao consultar saldo")

# Casos de teste
conta = ContaBancaria("Tiago", "12345")
conta.depositar(1000)
conta.sacar(200)
print(conta.consultar_saldo())

# Casos com erro
conta.depositar(-50)
conta.sacar("duzentos")
conta.sacar(2000)
