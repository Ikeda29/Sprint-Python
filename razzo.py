import random
import os
import time
import csv
import pandas as pd

""" Cores usadas no terminal"""
cores = {
    'reset': '\033[0m',
    'preto': '\033[30m',
    'vermelho': '\033[31m',
    'verde': '\033[32m',
    'amarelo': '\033[33m',
    'roxo': '\033[34m',
    'rosa': '\033[35m',
    'ciano': '\033[36m',
    'branco': '\033[37m'
}

saldo = 0  
"""Saldo inicial do usuário"""

"""Carregar códigos de convite de um arquivo CSV"""
codigos_convite = pd.read_csv('codigos_convite.csv')

def carregar_participantes(caminho_csv):
    participantes = []
    with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=';')
        for linha in leitor:
            participantes.append(linha['Participant'])
    return participantes

participantes = carregar_participantes('drivers_championship.csv')

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def voltar():
    input(cores['ciano'] + "\nPressione ENTER para continuar..." + cores["reset"])

def exibir_saldo(saldo: float):
    print(cores["amarelo"] + f"Seu saldo atual é: {saldo:.2f} moedas." + cores["reset"])

def obter_aposta(saldo: float):
    if saldo <= 0:
        print(cores["vermelho"] + "Você não tem saldo suficiente para apostar." + cores["reset"])
        voltar()
        return None
    
    while True:
        try:
            aposta = input(cores["ciano"] + "Digite o valor da sua aposta (ou 'v' para voltar): " + cores["reset"])
            if aposta.lower() == 'v':
                return None 
            aposta = float(aposta)
            if aposta <= 0:
                print(cores["vermelho"] + "A aposta deve ser um valor positivo." + cores["reset"])
            elif aposta > saldo:
                print(cores["vermelho"] + "Você não tem saldo suficiente para essa aposta." + cores["reset"])
                voltar()
                return None
            else:
                return aposta
        except ValueError:
            print("Entrada inválida. Por favor, digite um número ou 'v' para voltar.")

def obter_escolhas(participantes: list):
    escolhas = []
    for i in range(5):
        escolha = input(f"Digite qual será o {i+1}º colocado (ou pressione ENTER para parar): ").lower()
        if escolha == "":
            break
        escolhas.append(escolha)

    return escolhas

def simular_corrida(participantes):
    random.shuffle(participantes)
    return participantes

def contador(acertos, resultado_real):
    pontos = 0
    for i, acerto in enumerate(acertos):
        if acerto == resultado_real[i].lower():
            pontos += 5 - i  
    return pontos

def comprar_mais_moedas():
    print(cores["ciano"] + "\nOpções de compra de moedas:" + cores["reset"])
    print("1. Receber 100 moedas por R$ 10.00")
    print("2. Receber 50 moedas por R$ 5.00")
    print("3. Receber 25 moedas por R$ 2.50")

    while True:
        escolha = input(cores["ciano"] + "Escolha uma opção (1, 2 ou 3): " + cores["reset"])
        match escolha:
            case "1":
                return 100, 10.00
            case "2":
                return 50, 5.00
            case "3":
                return 25, 2.50
            case _:
                print(cores["vermelho"] + "Opção inválida. Por favor, escolha 1, 2 ou 3." + cores["reset"])

def validar_codigo_convite(codigo):
    if codigo in codigos_convite['codigo'].values:
        return True
    return False

def aplicar_codigo_convite():
    global saldo
    codigo = input(cores["ciano"] + "Digite seu código de convite: " + cores["reset"])
    
    if validar_codigo_convite(codigo):
        saldo += 100
        print(cores["verde"] + "Código válido! Você ganhou 100 moedas." + cores["reset"])
    else:
        print(cores["vermelho"] + "Código inválido. Tente novamente." + cores["reset"])

# Bloco principal
while True:
    limpar_terminal()
    print(cores["verde"] + "Bem-vindo ao RAZZO, jogo de apostas em corrida de Formula E!" + cores["reset"])
    print(cores["ciano"] + "\nMENU PRINCIPAL" + cores["reset"])
    print("1. Apostar")
    print("2. Verificar Saldo")
    print("3. Comprar mais moedas")
    print("4. Aplicar código de convite")
    print(cores["vermelho"] + "5. Sair" + cores["reset"])
    
    escolha = input(cores["ciano"] + "Escolha uma opção (1, 2, 3, 4 ou 5): " + cores["reset"])
    
    match escolha:
        case "1":
            limpar_terminal()
            aposta = obter_aposta(saldo)
            if aposta is None:
                continue

            """obter as apostas do usuário (até 5)"""
            print(f"\nEscolha até 5 participantes da lista: {', '.join(participantes)}")
            escolhas_usuario = obter_escolhas(participantes)
            
            if not escolhas_usuario:
                print(cores["vermelho"] + "Você não fez nenhuma escolha." + cores["reset"])
                voltar()
                continue

            """ Simular a corrida"""
            resultado_real = simular_corrida(participantes)
            print("\nResultados da corrida:")
            for i, carro in enumerate(resultado_real[:5]):
                print(f"{i+1}º: {carro}")
            
            """ Contar os acertos"""
            pontos = contador(escolhas_usuario, resultado_real[:5])
            print(f"\nVocê acertou {pontos} pontos.")
            
            if pontos > 0:
                saldo += aposta * pontos
                print(cores["verde"] + f"Parabéns! Você ganhou {aposta * pontos:.2f} moedas." + cores["reset"])
            else:
                saldo -= aposta
                print(cores["vermelho"] + f"Você perdeu {aposta:.2f} moedas." + cores["reset"])
            
            exibir_saldo(saldo)
            voltar()
        
        case "2":
            limpar_terminal()
            exibir_saldo(saldo)
            voltar()
        
        case "3":
            limpar_terminal()
            moedas, custo = comprar_mais_moedas()
            pagamento = input(cores["ciano"] + f"\nVocê deseja comprar {moedas} moedas por R$ {custo:.2f}? (s/n): " + cores["reset"])
            
            if pagamento.lower() == 's':
                saldo += moedas
                print(cores["verde"] + f"Você comprou {moedas} moedas com sucesso!" + cores["reset"])
            else:
                print(cores["vermelho"] + "Compra cancelada." + cores["reset"])
            
            exibir_saldo(saldo)
            voltar()

        case "4":  
            limpar_terminal()
            aplicar_codigo_convite()
            exibir_saldo(saldo)
            voltar()
        
        case "5":
            limpar_terminal()
            print(cores["verde"] + "Obrigado por jogar!" + cores["reset"])
            break
        
        case _:
            print(cores["vermelho"] + "Opção inválida. Por favor, escolha 1, 2, 3, 4 ou 5." + cores["reset"])
            voltar()
