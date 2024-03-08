import socket

UDP_IP = "10.1.1.16"
UDP_PORT = 49002

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

while True:
    data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
    #print("received message: %s" % data)
    print(data.hex())
    airData = hex(data[0])
    if airData=='0x81':
        print(airData)

    print('number of receiver  '+data[1:2])
    typeMessage = bin(data[6]) # 7 байт тип сообщения -> первые шесть бит: тип АДСБ, два последних: номер канала
    print(typeMessage)

    # для первого канала 0b00001100 - ADSB-112; 0b00001000 - ADSB-56; 0b00000100 - A/C
    # для второго канала 0b00001101 - ADSB-112; 0b00001001 - ADSB-56; 0b00000101 - A/C
    # для третьего канала 0b00001110 - ADSB-112; 0b00001010 - ADSB-56; 0b00000110 - A/C
    # для четвертого канала 0b00001111 - ADSB-112; 0b00001011 - ADSB-56; 0b00000111 - A/C
    if (data[6] ^ 0b00001100)==0b00000000:
        print('first channel - ADSB-112')
    if (data[6] ^ 0b00001000)==0b00000000:
        print('first channel - ADSB-56')
    if (data[6] ^ 0b00000100)==0b00000000:
        print('first channel - A/C')