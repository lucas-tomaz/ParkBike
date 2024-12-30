import serial
import serial.tools.list_ports
import time
from datetime import datetime

#FORMATO DO JSON PARA COLETA DE DADOS
#{"min": 40,"max": 50,"acquisitionTime": 1}  

# Função para enviar um dicionário via porta serial
def enviar_dicionario(arduino, dados):
    input("Pressione Enter para continuar...")
    arduino.write(str(dados).encode())
    print(f"Dados enviados: {dados}")

# Função para escutar e processar novos dados da porta serial
def escutar_porta_serial(arduino):
    start_time = time.time()
    #arquivo = open("dados_experimento.txt", "w")  # Abrir arquivo para escrita
    current_datetime = datetime.now()
    arquivo_nome = f"bike_trial_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    arquivo = open(arquivo_nome, "w")  # Abrir arquivo para escrita

    while (time.time() - start_time < dados["acquisitionTime"] * 60):
        # Tentar ler da porta serial
        dado = arduino.readline().decode().strip()
        
        if dado:  # Verificar se há um novo dado
            dados_separados = dado.split(',')  # Separar os dados por vírgula
            if len(dados_separados) == 3:
                dado0, dado1, dado2 =  int(dados_separados[0]), int(dados_separados[1]), dados_separados[2],
                print(f"{dado0}, {dado1}, {dado2}")
                arquivo.write(f"{dado0}, {dado1}, {dado2}\n")  # Escrever os dados no arquivo

    # Adicionar uma última linha com as informações solicitadas
    acq_time = dados["acquisitionTime"]
    arquivo.write(f"{dado0}, {acq_time * 60 * 1000}, 3\n")
    #arquivo.write(f"início do trial:{start_time}, fim do trial:{time.time()}")
    arquivo.close()  # Fechar o arquivo após a coleta de dados

# Procurar a porta COM do Arduino
def encontrar_porta_arduino():
    portas_disponiveis = list(serial.tools.list_ports.comports())
    porta_arduino = None

    for porta in portas_disponiveis:
        if "CH340" in porta.description:
            porta_arduino = porta.device
            break

    return porta_arduino

# Tentar encontrar a porta do Arduino
porta_arduino = encontrar_porta_arduino()

if porta_arduino is None:
    print("Arduino não detectado. Verifique a conexão USB.")
else:
    # Configurar a porta serial para comunicação com o Arduino
    arduino = serial.Serial(porta_arduino, 9600, timeout=1)
    time.sleep(0.1)  # Aguardar x segundos


    # Dicionário com os valores a serem enviados
    global dados
    dados = {"min": 40,"max": 50,"acquisitionTime": 2}  

    # Enviar o dicionário via porta serial
    enviar_dicionario(arduino, dados)

    # Iniciar o escutador da porta serial
    escutar_porta_serial(arduino)

    # Fechar a porta serial (Isso nunca será executado porque o escutador é um loop infinito)
    arduino.close()

'''

import serial
import serial.tools.list_ports
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Função para enviar um dicionário via porta serial
def enviar_dicionario(arduino, dados):
    input("Pressione Enter para iniciar a coleta...")
    arduino.write(str(dados).encode())
    print(f"Dados enviados: {dados}")

# Função para exibir o gráfico em tempo real
def animate(i):
    # Tentar ler da porta serial
    dado = arduino.readline().decode().strip()
    
    if dado:  # Verificar se há um novo dado
        dados_separados = dado.split(',')  # Separar os dados por vírgula
        if len(dados_separados) == 3:
            dado0, dado1, dado2 = map(int, dados_separados)
            print(f"{dado0}, {dado1}, {dado2}")
            x_data.append(i)
            y_data.append(dado2)
            ax.clear()
            ax.plot(x_data, y_data)
            ax.set_title("Valor de dado2 em tempo real")
            ax.set_xlabel("Tempo")
            ax.set_ylabel("dado2")
            ax.set_ylim(0, 4)
            ax.set_yticks([0, 1, 3, 2])
            ax.set_yticklabels(["", "AUMENTA", "OK", "DIMINUI"])

# Procurar a porta COM do Arduino
def encontrar_porta_arduino():
    portas_disponiveis = list(serial.tools.list_ports.comports())
    porta_arduino = None

    for porta in portas_disponiveis:
        if "CH340" in porta.description:
            porta_arduino = porta.device
            break

    return porta_arduino

# Tentar encontrar a porta do Arduino
porta_arduino = encontrar_porta_arduino()

if porta_arduino is None:
    print("Arduino não detectado. Verifique a conexão USB.")
else:
    # Configurar a porta serial para comunicação com o Arduino
    arduino = serial.Serial(porta_arduino, 9600, timeout=1)
    time.sleep(0.1)  # Aguardar x segundos

    # Dicionário com os valores a serem enviados
    global dados
    dados = {"min": 20,"max": 30,"acquisitionTime": 1}  

    # Enviar o dicionário via porta serial
    enviar_dicionario(arduino, dados)

    # Inicializar os dados para o gráfico em tempo real
    x_data = []
    y_data = []

    # Criar a figura e o eixo para o gráfico
    fig, ax = plt.subplots()

    # Iniciar a animação com save_count definido
    ani = animation.FuncAnimation(fig, animate, interval=10, save_count=100)  # Atualiza a cada 1 segundo

    # Mostrar a janela do gráfico
    plt.show()

    # Fechar a porta serial (Isso nunca será executado porque a animação é um loop infinito)
    arduino.close()

    '''
