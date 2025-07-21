# Trabalho teórico-prático de Redes de Computadores

## Alunos:
- Ítalo Aurélio de Paula Vieira
- Rodrigo Júnio Lanchin de Almeida

## Linguagem:
- Python

---

## Como rodar:

---

## Explicação detalhada do código:

### Receptor (receptor.py)

```python
import socket
```

Importa o módulo `socket`, que permite criar conexões de rede. É a base para qualquer comunição de rede em Python

```python
HOST = '127.0.0.1'
PORT = 5005
```
Define o endereço IP e a porta que o receptor vai usar para escutar mensagens

- `'127.0.0.1'` é o IP de **localhost**, ou seja, o receptor só escuta mensagens vindas da própia máquina.
- `5005` é a **porta** que escolhemos para comunicação, mas não há nenhuma regra para a escolha da mesma, poderia ser qualquer uma entre 1024 e 65535

Obs: o número máximo de portas é 65535 por conta das portas serem codificadas em 16 bits, ou seja de `00000000 00000000` (porta 0) até `11111111 11111111` (porta 65535). As portas de **0** a **1023** são portas bem conhecidas, usadas para outras funcionalidades, como:

- `80`: HTTP
- `443`: HTTPS
- `21`: FTP
- `22`: SSH

Logo, o ideal é usar de 1024 para frente para evitar bater em alguma dessas portas.

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

Cria o socket(canal de comunicação) que será usado para receber dados:

- `AF_INET` define que vamos usar o protocolo IPv4 (Afim de simplificar o projeto, fazendo com que os testes possam ser feitos locais, sem conexão com a internet).
- `SOCK_DGRAM` define que o protocolo de transporte será o **UDP** (Mais rápido, menos confiável, pois envia a mensagem sem interesse no resultado, não sabe se chegou ou não, não necessita de conexão para teste, tem tamanho limitado e cabeçalho de apenas 8 bytes).

```python
sock.bind((HOST,PORT))
```

Vincula o socket ao IP e à porta definidos. A partir daqui o receptor está escutando nessa porta, pronto para receber mensagens.

```python
sock.settimeout(1.0)
```

Adiciona uma valor de timeout para depois conseguir parar a execução do programa.

```python
print(f"[Receptor] Aguardando mensagens em {HOST}:{PORT}")
```

Imprime no terminal uma mensagem informando que o receptor está pronto e em qual IP/porta ele está escutando.

```python
try:
    {...}
except socket.timeout:
    continue
```

Faz com que o receptor pare o processor de 1 em 1 segundo baseado no tempo que foi definido mais acima no código para ouvir a fim de que um pouco mais a frente no código ele possa ouvir o teclado para terminar o processo caso seja nescessário.

```python
while True:
    try:
        data, addr = sock.recvfrom(1024)
        print(f"[Receptor] Recebido de {addr}: {data.decode()}")
```
- `while True:` cria um loop infinito para que o receptor fique sempre escutando.

- `sock.recvfrom(1024)` aguarda o recebimento de uma mensagem de no máximo 1024 bytes que retorna 2 valores:
    - `data`: o conteúdo da mensagem.
    - `addr`: o endereço (IP, porta) de quem enviou.
    - A função `sock.recvfrom(1024)` já retornar um array com 2 valores([0] e [1]), o que fazemos é apenas separar esses valores agora, antes que tenhamos que separar mais tarde.

- `data.decode()` converte os bytes recebidos para texto (string).

- A mensagem e o remetente são então impressos na tela

```python
try:
    {...}
except KeyboardInterrupt:
    print("[Receptor] Encerado pelo usuário.")
    sock.close()
```

De segundo em segundo ele sai do `try` e vê se o usuário fez algum imput no teclado, nesse caso, o input padrão para cancelar um código que está sendo executado é `Ctrl + C`, logo, se o usuário realizar esse input, o receptor para de rodar.