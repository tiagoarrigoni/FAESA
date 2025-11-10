# retangulo_modulo.py

class Retangulo:
    def __init__(self, largura, altura):
        try:
            if not isinstance(largura, (int, float)) or not isinstance(altura, (int, float)):
                raise TypeError("Largura e altura devem ser numeros")
            if largura <= 0 or altura <= 0:
                raise ValueError("Largura e altura devem ser maiores que zero")
        except (TypeError, ValueError) as e:
            print("Erro ao criar retangulo:", e)
            raise
        else:
            self.largura = largura
            self.altura = altura

    @property
    def area(self):
        return self.largura * self.altura

    @property
    def perimetro(self):
        return 2 * (self.largura + self.altura)

    def eh_quadrado(self):
        return self.largura == self.altura


# Casos de teste
if __name__ == "__main__":
    try:
        r1 = Retangulo(5, 5)
        print("Area:", r1.area)
        print("Perimetro:", r1.perimetro)
        print("Eh quadrado?", r1.eh_quadrado())
    except Exception as e:
        print("Erro:", e)

    # Casos com erro
    try:
        r2 = Retangulo(-2, "dez")
    except Exception as e:
        print("Excecao capturada:", e)
