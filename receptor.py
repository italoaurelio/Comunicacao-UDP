import socket

HOST = '127.0.0.1'
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1.0)

print(f"[Receptor] Aguardando mensagens em {HOST}:{PORT}")

ultimo_num_receb = -1

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode()
            
            partes = msg.split("|")
            
            if len(partes) != 2:
                print("[Receptor] Mensagem mal formatada.")
                continue
            numero_seq = int(partes[0])
            conteudo = partes[1]
            
            if numero_seq != ultimo_num_receb:
                print(f"[Receptor] Nova mensagem recebida de {addr}:\n      - Sequência={numero_seq}\n      - Conteúdo='{conteudo}")
                ultimo_num_receb = numero_seq
                
                ack = f"ACK:{numero_seq}"
                sock.sendto(ack.encode(), addr)
            else:
                print(f"[Receptor] Duplicata detectada (seq={numero_seq})")
                ack = f"ACK:{numero_seq}"
                sock.sendto(ack.encode(), addr)
                            
        except socket.timeout:
                continue

except KeyboardInterrupt:
    print("[Receptor] Encerado pelo usuário.")
    sock.close()