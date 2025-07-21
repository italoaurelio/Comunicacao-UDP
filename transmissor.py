import socket
import time

HOST = '127.0.0.1'
PORT = 5005

numero_sequencia = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

print("[Transmissor] Digite uma mensagem ('Ctrl + c' ou 'sair' para encerrar):")

try:
    while True:
        msg = input("[Mensagem] >> ")
        msg_format = f"{numero_sequencia}|{msg}"
        if msg.lower() == 'sair':
            break
        
        while True:
            sock.sendto(msg_format.encode(), (HOST, PORT))
            print(f"[Transmissor] Enviada: {msg_format}")
            
            try:
                ack_data, _ = sock.recvfrom(1024)
                ack_menssage = ack_data.decode()
                
                if ack_menssage == f"ACK:{numero_sequencia}":
                    print("[Transmissor] ACK recebido! Enviando próxima...")
                    numero_sequencia = 1 - numero_sequencia
                    break
                else:
                    print("[Transmissor] ACK incorreto, retransmitindo...")
                    
            except socket.timeout:
                i = 0
                while i<5:
                    print("[Transmissor] Timeout! Retransmitindo...")
                    i+=1
            
            except ConnectionResetError:
                i = 0
                while i<5:
                    print("[Transmissor] Receptor não disponível. Tentando novamente em 2 segundos...")
                    time.sleep(2)
                    i+=1
            break


except KeyboardInterrupt:
    print("\n[Transmissor] Encerrado pelo usuário.")
    sock.close()