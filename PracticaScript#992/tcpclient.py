import socket

target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[*] Intentando conectar a {target_host}:{target_port}...")
client.connect((target_host, target_port))
print("[*] ¡Conexión exitosa!")

client.send(b"Hola desde el cliente TCP!")

response = client.recv(4096)
print(f"[*] El servidor respondió: {response.decode()}")