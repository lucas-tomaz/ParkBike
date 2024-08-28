import tkinter as tk
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import time
from datetime import datetime
from tkinter import messagebox as msg

class ImageViewer:
    def __init__(self, root, initial_x=0):
        self.root = root
        self.root.title("PARK_BIKE")

        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=50, pady=50)

        self.counter_label = tk.Label(self.root, text="Valor atual de RPM: 0")
        self.counter_label.pack(pady=10)
        self.dados = []

        self.x = initial_x  # Inicializa o contador x com o valor inicial

        self.start_time = None

        self.cronometro()


    def update_image(self, dado0):
        self.x = dado0  # Atualiza o valor do contador x com o valor dado0

        if self.x > 50:
            image_path = "C:\\Users\Laboratorio\\Documents\\ParkBike\\static\\seta_para_baixo(1).png"
        elif self.x < 40:
            image_path = "C:\\Users\\Laboratorio\\Documents\\ParkBike\\static\\seta_para_cima(1).png"
        else:
            image_path = "C:\\Users\\Laboratorio\\Documents\\ParkBike\\static\\ok.png"

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Atualiza o rótulo do contador
        self.counter_label.config(text=f"Valor atual RPM: {self.x}")

    def wait_and_continue_loop(self):
        # Agendando a próxima atualização após 50 milissegundos (2 segundos)
        self.root.after(50, self.listen_and_update) 

    def listen_and_update(self):
        dado = arduino.readline().decode().strip()
        if dado:
            dados_separados = dado.split(',')
            if len(dados_separados) == 3:
                dado0 = int(dados_separados[0])
                print(f"{dado0}, {dados_separados[1]}, {dados_separados[2]}")
                self.dados.append((dados_separados[0], dados_separados[1], dados_separados[2]))
                # Atualiza a imagem com base no valor de dado0
                self.update_image(dado0)

        # Aguarda 50 milissegundo antes de iniciar o próximo loop
        self.root.after(25, self.wait_and_continue_loop)

    def cronometro(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.root.title(f"PARK_BIKE | Tempo decorrido: {int(elapsed_time)} segundos")
            if elapsed_time < 120:
                self.root.after(1000, self.cronometro)
            else:
                button_finalizar = tk.Button(root, text="Finalizar Experimento", command= termino)
                button_finalizar.pack()

def enviar_dicionario(arduino, dados):
    arduino.write(str(dados).encode())
    print(f"Dados enviados: {dados}")

def escutar_porta_serial(arduino):
    print("Escrevendo os dados")
    start_time = time.time()
    current_datetime = datetime.now()
    arquivo_nome = f"bike_trial_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    arquivo = open(arquivo_nome, "w")  # Abrir arquivo para escrita

    while (time.time() - start_time < dados["acquisitionTime"] * 60):
        # Tentar ler da porta serial
        dado = arduino.readline().decode().strip()

        if dado:  # Verificar se há um novo dado
            dados_separados = dado.split(',')  # Separar os dados por vírgula
            if len(dados_separados) == 3:
                dado0, dado1, dado2 =  int(dados_separados[0]), int(dados_separados[1]), dados_separados[2]
                print(f"{dado0}, {dado1}, {dado2}")
                arquivo.write(f"{dado0}, {dado1}, {dado2}\n")  # Escrever os dados no arquivo

    # Adicionar uma última linha com as informações solicitadas
    acq_time = dados["acquisitionTime"]
    arquivo.write(f"{dado0}, {acq_time * 60 * 1000}, 3\n")
    arquivo.close()  # Fechar o arquivo após a coleta de dados

def salvar_dados(dados_lidos):
    start_time = time.time()
    current_datetime = datetime.now()
    arquivo_nome = f"bike_trial_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    arquivo = open(arquivo_nome, "w")  # Abrir arquivo para escrita

    for dado in dados_lidos:
        dado0, dado1, dado2 =  int(dado[0]), int(dado[1]), dado[2]
        arquivo.write(f"{dado0}, {dado1}, {dado2}\n")  # Escrever os dados no arquivo

    # Adicionar uma última linha com as informações solicitadas
    acq_time = dados["acquisitionTime"]
    arquivo.write(f"{dado0}, {acq_time * 60 * 1000}, 3\n")
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

def inicio():
    app.start_time = time.time()
    app.cronometro()
    enviar_dicionario(arduino,dados)

def termino():
    root.destroy()
    salvar_dados(app.dados)
    print("Dados salvos com sucesso.")

def fechar_janela():
    if msg.askyesno("Desativar Janela", "Deseja sair sem salvar?"):
        root.destroy()

def erro_conexao():
    msg.showerror("Conexao USB","Arduino não detectado. Verifique a conexão USB.")

# Tentar encontrar a porta do Arduino
porta_arduino = encontrar_porta_arduino()

if porta_arduino is None:
    erro_conexao()
    print("Arduino não detectado. Verifique a conexão USB.")
else:
    arduino = serial.Serial(porta_arduino, 9600, timeout=1)
    time.sleep(0.1)

    dados = {"min": 40, "max": 50, "acquisitionTime": 2}

    root = tk.Tk()
    app = ImageViewer(root)

    # Iniciar o primeiro loop após a inicialização da interface
    app.wait_and_continue_loop()

    button_iniciar = tk.Button(root, text="Iniciar Experimento", command= inicio)
    button_iniciar.pack()

    #CONFIGURACAO PARA EVITAR FECHAR A JANELA DE CONEXAO:
    root.protocol("WM_DELETE_WINDOW",fechar_janela)

    root.mainloop()

    # Fechar a porta serial
    arduino.close()