import pandas as pd
import random
import string

def gerar_codigo(length=10):
    """Gera um código aleatório com letras e números."""
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

def gerar_codigos_csv(num_codigos=100, nome_arquivo='codigos_convite.csv'):
    """Gera um DataFrame com códigos e salva em um arquivo CSV."""
    codigos = [gerar_codigo() for _ in range(num_codigos)]
    df = pd.DataFrame({'codigo': codigos})
    df.to_csv(nome_arquivo, index=False)

if __name__ == "__main__":
    gerar_codigos_csv(100)  # Gera 100 códigos aleatórios
