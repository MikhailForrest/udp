import socket
import math
import myFunc
from crc import Calculator, Crc32

UDP_IP = "10.1.1.16"
UDP_PORT = 49002

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print(data.hex())
    airData = hex(data[0])
    if airData=='0x81':
        print('=======================================================')
        line_str = ''
        line_str += 'number of receiver  '+str(int(data[2:4].hex(),16))+'; '
        line_str += 'level  '+str(40-int(data[15:16].hex(),16))+'; ' 
        line_str += 'SNR  '+str(2+20*math.log10(int(data[16:17].hex(),16)))+'; '
        
        print (line_str) # проверка: можно ли два байта брать такой записью

        #typeMessage = bin(data[6]) # 7 байт тип сообщения -> первые шесть бит: тип АДСБ, два последних: номер канала
        #print(typeMessage)

        # потом перенести в отжельную функцию
        # для первого канала 0b00001100 - ADSB-112; 0b00001000 - ADSB-56; 0b00000100 - A/C
        # для второго канала 0b00001101 - ADSB-112; 0b00001001 - ADSB-56; 0b00000101 - A/C
        # для третьего канала 0b00001110 - ADSB-112; 0b00001010 - ADSB-56; 0b00000110 - A/C
        # для четвертого канала 0b00001111 - ADSB-112; 0b00001011 - ADSB-56; 0b00000111 - A/C
        # if (data[6] ^ 0b00001100)==0b00000000:
        #     print('first channel - ADSB-112')
        # elif (data[6] ^ 0b00001000)==0b00000000:
        #     print('first channel - ADSB-56')
        # elif (data[6] ^ 0b00000100)==0b00000000:
        #     print('first channel - A/C')
        # elif (data[6] ^ 0b00001101)==0b00000000:
        #     print('Second channel - ADSB-112')
        # elif (data[6] ^ 0b00001001)==0b00000000:
        #     print('Second channel - ADSB-56')
        # elif (data[6] ^ 0b00000101)==0b00000000:
        #     print('Second channel - A/C')
        # elif (data[6] ^ 0b00001110)==0b00000000:
        #     print('Third channel - ADSB-112')
        # elif (data[6] ^ 0b00001010)==0b00000000:
        #     print('Third channel - ADSB-56')
        # elif (data[6] ^ 0b00000110)==0b00000000:
        #     print('Third channel - A/C')   
        # elif (data[6] ^ 0b00001111)==0b00000000:
        #     print('Forth channel - ADSB-112')
        # elif (data[6] ^ 0b00001011)==0b00000000:
        #     print('Forth channel - ADSB-56')
        # elif (data[6] ^ 0b00000111)==0b00000000:
        #     print('Forth channel - A/C')
        print(myFunc.byteToTypeAndNumberOfChannel(data[6]))
        calc = Calculator(Crc32.CRC32,optimized=True)
        #assert data[-2:]==calc.checksum(data[:-2])


        if (data[6] ^ 0b00001100)==0b00000000:
            adsb_112_Data = data[17:31]
            print(adsb_112_Data.hex())
            print('ICAOaddress   '+adsb_112_Data[1:4].hex())