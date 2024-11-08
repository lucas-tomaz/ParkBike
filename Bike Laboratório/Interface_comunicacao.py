import serial

# Configuração da porta serial (substitua o valor de 'COMx' ou '/dev/ttyUSBx' conforme o seu sistema)
# Para Windows, pode ser algo como 'COM3'. No Linux ou MacOS, algo como '/dev/ttyUSB0'
arduino = serial.Serial('COM3', 9600, timeout=1)  # Ajuste a porta serial conforme necessário

# Função para ler e processar os dados recebidos pela porta serial
def read_serial():
    while True:
        # Lê uma linha da porta serial (enquanto houver dados disponíveis)
        line = arduino.readline().decode('utf-8').strip()  # Lê e decodifica a linha
        
        if line:  # Se a linha não estiver vazia
            # Divide a linha em três partes, separadas por vírgulas
            try:
                valor1, valor2, valor3 = line.split(',')
                valor1 = float(valor1)  # RPM (convertido para float)
                valor2 = int(valor2)    # Tempo (convertido para int)
                # O valor3 já está como string, com o status (AUTO, BAIXO ou OK)
                
                # Exibe os valores recebidos
                print(f"RPM: {valor1}, Tempo: {valor2}, Status: {valor3}")
            except ValueError:
                print("Erro ao processar a linha recebida.")
        else:
            print("Sem dados recebidos.")
            
# Chama a função de leitura
read_serial()
