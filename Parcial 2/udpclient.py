import socket

target_host = "8.8.8.8"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"AAABBBCCC", (target_host, target_port))

data, addr = client.recvfrom(4096)

print(data)