import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import messagebox as msg



class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Gráfica - Teste")
        self.root.geometry("640x440")

        self.image_label = tk.Label(root)
        self.image_label.pack(padx=60, pady=60)

        self.counter_label = tk.Label(root, text="Valor atual de RPM: 0")
        self.counter_label.pack(pady=30)

        self.x = 0  # Inicializa o contador x
        #input("Pressione Enter para continuar")
        
        self.start_time = None
        self.cronometro()

        button_iniciar = tk.Button(root, text="Iniciar Experimento", command= self.iniciar, bg="green", fg="white", font=("Arial", 10, "bold"))
        button_iniciar.pack()

        #button_iniciar = tk.Button(root, text="Finalizar Experimento", command= self.salvar_dados)
        #button_iniciar.pack()

        #self.cronometro()
    
    def iniciar(self):
        self.start_time = time.time()
        self.update_image()

    def salvar_dados(self):
        self.root.destroy()
        print("Dados Salvos com sucesso!")

    def update_image(self):

        self.x += 1  # Incrementa o valor do contador x

        if self.x > rpm_maximo:
            image_path = "C:\\Users\Laboratorio\\Documents\\ParkBike\\static\\seta_para_baixo_preta.jpg"
        elif self.x < rpm_minimo:
            image_path = "C:\\Users\Laboratorio\\Documents\\ParkBike\\static\\seta_para_cima_preta.jpg"
        else:
            image_path = "C:\\Users\Laboratorio\\Documents\\ParkBike\\static\\ok.png"

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        # Atualiza o rótulo do contador
        self.counter_label.config(text=f"Valor atual de RPM: {self.x}")

        # Agendando a próxima atualização após 1000 milissegundos (1 segundo)
        self.root.after(1000, self.update_image)
        
    def cronometro(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.root.title(f"Interface Gráfica - Teste | Tempo decorrido: {int(elapsed_time)} segundos")
            if elapsed_time < tempo_experimento:
                self.root.after(1000, self.cronometro)
            else:
                button_finalizar = tk.Button(root, text="Finalizar Experimento", command= self.salvar_dados, bg="red", fg="white", font=("Arial", 10, "bold"))
                button_finalizar.pack()
        else:
            self.root.after(50, self.cronometro)

class solicitar_dados:
    def __init__(self,janela):
        self.janela = janela
        self.janela.title("Interface de Configuracao")
        self.janela.configure(bg="gray")
        self.janela.geometry("640x300")

        self.label_title = tk.Label(janela, text="🚲 Sistema CadBike 🚲", bg="gray",fg="white", font=("Times New Roman",24, "bold"))
        self.label_title.pack(pady=10)

        frame_parametros = tk.Frame(janela, bg="gray")
        frame_parametros.pack(pady=30)

        self.label_rpm_minimo = tk.Label(frame_parametros, text="RPM Minimo:", bg="gray", fg="white", font=("Arial", 12, "bold"))
        self.label_rpm_minimo.grid(row=0,column=0)

        self.entry_rpm_minimo = tk.Entry(frame_parametros)
        self.entry_rpm_minimo.grid(row=0,column=1)

        self.label_rpm_maximo = tk.Label(frame_parametros, text="RPM Maximo:",bg="gray", fg="white", font=("Arial", 12, "bold"))
        self.label_rpm_maximo.grid(row=1,column=0)

        self.entry_rpm_maximo = tk.Entry(frame_parametros)
        self.entry_rpm_maximo.grid(row=1,column=1)

        self.label_tempo_experimento = tk.Label(frame_parametros, text="Tempo de Experimento(segundos):", bg="gray", fg="white", font=("Arial", 12, "bold"))
        self.label_tempo_experimento.grid(row=2,column=0)
        self.entry_tempo_experimento = tk.Entry(frame_parametros)
        self.entry_tempo_experimento.grid(row=2,column=1)

        ok_button = tk.Button(frame_parametros, text="Abrir Interface", command=self.fechar_janela, bg="green", fg="white", font=("Arial", 10, "bold"))
        ok_button.grid(row=3, column=0, columnspan=2)

    def obter_dados(self):
        valor_rpm_minimo = self.entry_rpm_minimo.get()
        valor_rpm_maximo = self.entry_rpm_maximo.get()
        valor_tempo_experimento = self.entry_tempo_experimento.get()

        global rpm_minimo, rpm_maximo, tempo_experimento
        rpm_minimo = int(valor_rpm_minimo)
        rpm_maximo = int(valor_rpm_maximo)
        tempo_experimento = int(valor_tempo_experimento)

    def fechar_janela(self):
        self.obter_dados()
        self.janela.destroy()


def fechar_janela():
    if msg.askyesno("Quit", "Deseja sair sem salvar?"):
        root.destroy()

def erro_conexao():
    msg.showerror("Informacao", "Porta nao encontrada.")



if __name__ == "__main__":
    #start_time = time.time()

    janela = tk.Tk()
    interface = solicitar_dados(janela)
    janela.mainloop()

    root = tk.Tk()
    app = ImageViewer(root)
    root.protocol("WM_DELETE_WINDOW",fechar_janela)
    root.mainloop()