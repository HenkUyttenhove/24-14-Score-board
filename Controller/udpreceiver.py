import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",1000))
sock.sendto("life",("172.16.1.10",1000))
while True:
    data, addr = sock.recvfrom(10)
    print("ontvangen:",data)
