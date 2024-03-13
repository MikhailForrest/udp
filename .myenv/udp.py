import socket
import math
import myFunc
from crc import Calculator, Crc16

UDP_IP = "10.1.1.16"
UDP_PORT = 49002

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

numOf112 = 0 # счетчик для количества 112 битных пакетов
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
        line_str += 'NumOfPack  '+str(int(data[4:6].hex(),16))+'; '
        line_str += 'CountOfMess  '+str(int(hex(data[1]),16))+'; '

        print (line_str) # проверка: можно ли два байта брать такой записью

        print(myFunc.byteToTypeAndNumberOfChannel(data[6]))
        calc = Calculator(Crc16.CCITT)
        chckSm = calc.checksum(data[0:len(data)-2])
        #print((chckSm))

        if (data[6] ^ 0b00001100)==0b00000000:
            adsb_112_Data = data[17:31]         
            if ((adsb_112_Data[0]>>2) ^ 0b100011)==0b00000: # проверка df17 - первые шесть бит первого байта
                print(adsb_112_Data.hex())
                ME_in_bytes = adsb_112_Data[4:11]
                #print(ME_in_bytes.hex())
                if ((ME_in_bytes[2] | 0b11111011) ^ 0b11111111) == 0b00000000: #смотрим 6-ой бит в третьем байте MESSAGE
                    print ("CPR odd (1)")
                else:
                    print ("CPR even (0)") 
                print('ICAOaddress   '+adsb_112_Data[1:4].hex())
                numOf112 +=1
            else:
                print((adsb_112_Data[0]>>2))
        
        if numOf112 >10:
            break