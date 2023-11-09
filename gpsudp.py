import socket
import errno

# General config
UDP_IP = "192.168.43.157"  # Change to your ip
UDP_PORT = 8888
MESSAGE_LENGTH = 32768  # one sensor data frame has 13 bytes

# Prepare UDP
print("This PC's IP: ", UDP_IP)
print("Listening on Port: ", UDP_PORT)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind((UDP_IP, UDP_PORT))
h=True
# Read data forever
while h:
    # Get latest data
    keepReceiving = True
    newestData = None
    while keepReceiving:
        try:
            data, fromAddr = sock.recvfrom(MESSAGE_LENGTH)
            if data:
                newestData = data.decode()
        except socket.error as why:
            if why.args[0] == errno.EWOULDBLOCK:
                keepReceiving = False
            else:
                raise why
    if newestData is not None:
        print(newestData)
        