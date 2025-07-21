import socket

HOST = '127.0.0.1'
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.settimeout(1.0)

print(f"[Receptor] Aguardando mensagens em {HOST}:{PORT}")

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(f"[Receptor] Recebido de {addr}: {data.decode()}")
        except socket.timeout:
                continue

except KeyboardInterrupt:
    print("[Receptor] Encerado pelo usuário.")
    sock.close()