# Trabalho teórico-prático de Redes de Computadores

## Alunos:
- Ítalo Aurélio de Paula Vieira
- Rodrigo Júnio Lanchin de Almeida

## Linguagem:
- Python

---

## Como rodar:

### Requisitos:

- Ter Python3 instalado;
- Ter um terminal.

### Execução

- Clone esse repósitório com:

```bash
git clone https://github.com/italoaurelio/Comunicacao-UDP
```

- Entre na pasta clonada com:

```bash
cd Comunicacao-UDP
```

- Você terá que rodar duas instâncias do terminal, uma com o transmissor e outra com o receptor:

    - Transmissor: `python transmissor.py`
    - Receptor: `python receptor`

Agora basta interagir com o transmissor e conferir os resultados no transmissor.
Para parar a execução de ambos, basta apertar `crtl + c` no terminal, ou escrever `'sair'` no transmissor.

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

### Transmissor (transmissor.py)

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

Cria um socket UDP:

- `AF_INET` → usa IPv4.
- `SOCK_DGRAM` → usa UDP.

Esse é o canal de envio de mensagens

```python
print("[Transmissor] Digite uma mensagem (ou 'sair' para encerrar):")
```

Mostra uma mensagem.

```python
while True:
    msg = input(">> ")
```

Loop que **lê mensagens do teclado**, uma por vez.

```python
if msg.lower() == 'sair':
    break
```

Se o usuário digitar `'sair'`, encerra o loop.

```python
sock.send(msg.encode(), (HOST, PORT))
```

Envia o que foi digitado para o IP e PORTA cadastrados no começo do código, que caso for o mesmo que o cadastrado no receptor, vai fazer com que a chamada chegue no mesmo.

- `msg.encode()` → converte a string para bytes (Obrigatório para UDP).
- `(HOST, PORT)` → define o endereço do receptor.

```python
ultimo_num_receb = -1
```

Define uma variável para controlar o **número de sequência** da última mensagem recebida. Inicializada com `-1` para garantir que a primeira mensagem (sequência 0) seja sempre aceita.

```python
try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode()
```

- O **primeiro `try`** captura interrupções do teclado (`Ctrl + C`).
- `while True:` mantém o receptor sempre escutando.
- O **segundo `try`** captura timeouts do socket.
- `data, addr = sock.recvfrom(1024)` recebe mensagens de até 1024 bytes.
- `msg = data.decode()` converte os bytes recebidos para string.

```python
partes = msg.split("|")

if len(partes) != 2:
    print("[Receptor] Mensagem mal formatada.")
    continue
numero_seq = int(partes[0])
conteudo = partes[1]
```

**Processa o formato da mensagem** que deve seguir o padrão `"numero_sequencia|conteudo"`:

- `msg.split("|")` divide a mensagem usando `|` como separador.
- Verifica se a mensagem tem exatamente 2 partes (número de sequência + conteúdo).
- Se mal formatada, ignora a mensagem e continua escutando.
- `numero_seq = int(partes[0])` extrai o número de sequência.
- `conteudo = partes[1]` extrai o conteúdo da mensagem.

```python
if numero_seq != ultimo_num_receb:
    print(f"[Receptor] Nova mensagem recebida de {addr}:\n      - Sequência={numero_seq}\n      - Conteúdo='{conteudo}")
    ultimo_num_receb = numero_seq
    
    ack = f"ACK:{numero_seq}"
    sock.sendto(ack.encode(), addr)
else:
    print(f"[Receptor] Duplicata detectada (seq={numero_seq})")
    ack = f"ACK:{numero_seq}"
    sock.sendto(ack.encode(), addr)
```

**Controle de duplicatas e envio de ACK**:

- **Se for uma nova mensagem** (número de sequência diferente do último recebido):
  - Exibe a mensagem formatada com sequência e conteúdo.
  - Atualiza `ultimo_num_receb` com o novo número.
  - Envia ACK de confirmação.

- **Se for uma duplicata** (mesmo número de sequência):
  - Apenas informa que detectou duplicata.
  - **Ainda assim envia ACK** para confirmar que recebeu (importante para o protocolo).

```python
except socket.timeout:
    continue
```

**Tratamento de timeout**: Se não receber nenhuma mensagem em 1 segundo, continua o loop. Isso permite verificar periodicamente se o usuário quer encerrar o programa.

```python
except KeyboardInterrupt:
    print("[Receptor] Encerado pelo usuário.")
    sock.close()
```

**Encerramento do programa**: Captura `Ctrl + C`, exibe mensagem de encerramento e fecha o socket corretamente.

### Transmissor (transmissor.py)

```python
import socket
import time
```

Importa os módulos necessários:
- `socket` → para comunicação de rede.
- `time` → para pausas e delays.

```python
HOST = '127.0.0.1'
PORT = 5005
```

Define o mesmo IP e porta do receptor para estabelecer comunicação.

```python
numero_sequencia = 0
```

Inicializa o **número de sequência** em 0. Este número alterna entre 0 e 1 para cada mensagem enviada, permitindo detectar duplicatas.

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)
```

Cria um socket UDP e define **timeout de 2 segundos** para aguardar ACKs do receptor.

```python
print("[Transmissor] Digite uma mensagem ('Ctrl + c' ou 'sair' para encerrar):")
```

Exibe instruções para o usuário.

```python
try:
    while True:
        msg = input("[Mensagem] >> ")
        msg_format = f"{numero_sequencia}|{msg}"
        if msg.lower() == 'sair':
            break
```

- **Loop principal** para leitura de mensagens.
- `msg_format = f"{numero_sequencia}|{msg}"` → **formata a mensagem** com número de sequência seguido de `|` e o conteúdo.
- Verifica se o usuário digitou `'sair'` para encerrar.

```python
while True:
    sock.sendto(msg_format.encode(), (HOST, PORT))
    print(f"[Transmissor] Enviada: {msg_format}")
```

**Loop de retransmissão**: Envia a mensagem formatada para o receptor e informa o envio.

```python
try:
    ack_data, _ = sock.recvfrom(1024)
    ack_menssage = ack_data.decode()
    
    if ack_menssage == f"ACK:{numero_sequencia}":
        print("[Transmissor] ACK recebido! Enviando próxima...")
        numero_sequencia = 1 - numero_sequencia
        break
    else:
        print("[Transmissor] ACK incorreto, retransmitindo...")
```

**Aguarda e verifica ACK**:

- Tenta receber confirmação do receptor.
- **Se o ACK for correto** (contém o número de sequência atual):
  - Confirma recebimento.
  - **Alterna o número de sequência** (0→1 ou 1→0) usando `1 - numero_sequencia`.
  - Sai do loop de retransmissão.
- **Se o ACK for incorreto**: Prepara para retransmitir.

```python
except socket.timeout:
    i = 0
    while i<5:
        print("[Transmissor] Timeout! Retransmitindo...")
        i+=1
```

**Tratamento de timeout**: Se não receber ACK em 2 segundos, exibe mensagem de timeout e prepara retransmissão (repete até 5 vezes).

```python
except ConnectionResetError:
    i = 0
    while i<5:
        print("[Transmissor] Receptor não disponível. Tentando novamente em 2 segundos...")
        time.sleep(2)
        i+=1
break
```

**Tratamento de erro de conexão**: Se o receptor não estiver disponível, aguarda 2 segundos antes de tentar novamente (repete até 5 vezes).

```python
except KeyboardInterrupt:
    print("\n[Transmissor] Encerrado pelo usuário.")
    sock.close()
```

**Encerramento do programa**: Captura `Ctrl + C`, exibe mensagem e fecha o socket adequadamente.

---

## Funcionamento do Protocolo

Este projeto implementa um **protocolo simples de controle de confiabilidade** sobre UDP:

1. **Numeração de sequência**: Cada mensagem recebe um número (0 ou 1) que alterna a cada envio.

2. **Confirmação (ACK)**: O receptor confirma cada mensagem recebida enviando um ACK com o número de sequência.

3. **Detecção de duplicatas**: O receptor ignora mensagens com números de sequência já processados.

4. **Retransmissão**: Se o transmissor não receber ACK em 2 segundos, reenvia a mensagem.

5. **Tolerância a falhas**: O sistema tenta reconectar automaticamente em caso de problemas de rede.